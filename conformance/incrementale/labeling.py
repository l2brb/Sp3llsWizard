import sys
import os
import json, copy, math
from pathlib import Path
from itertools import product
from collections import defaultdict

# Add src to PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils import petri_parser


# INTPUT WN
pnml_file_path = "/home/l2brb/main/DECpietro/conformance/wnsample/wn_nfa.pnml"  
workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
#print(workflow_net)


# ------------------------------------------------------------------
# Mapping sulla WN : transition ids  ->  labels

Map = {}

for tr in workflow_net["transitions"]:
    # se la transizione è silente, etichettala con 'τ' (tau)
    label = "τ" if tr["is_tau"] else tr["name"]
    Map[tr["id"]] = label
print(Map)


# helper per tradurre id → label
def id2lab(tid):                      
    return Map.get(tid, "?")



# ------------------------------------------------------------------
# Reader della traccia 
# Traccia input #TODO: solo un test per ora ci devo buttare un log parser sopra
input_trace = ["A", "C", "A", "F", "B", "K", "M", "J", "B"]




# ------------------------------------------------------------------
# L^-1 relabeling

L_inv = {}                      
for t_id, lab in Map.items():
    if lab not in L_inv:        
        L_inv[lab] = []          
    L_inv[lab].append(t_id)  

#print("----------------------")
#print("L^-1:", dict(L_inv))



# ------------------------------------------------------------------
# L^-1 labeling della traccia

labels_in_trace = set(input_trace)

L_inv = {lab: L_inv[lab]                  # stesso oggetto lista
         for lab in labels_in_trace
         if lab in L_inv}                 # ignora label “sconosciute”

#print("L⁻¹ labeling della traccia", L_inv)



# ------------------------------------------------------------------
# Json della DecSpec 
declare_path = Path("/home/l2brb/main/DECpietro/conformance/wnsample/wn_nfa.json")   
model_json   = json.loads(declare_path.read_text())

#print("Model JSON:", model_json)









# ------------------------------------------------------------------
# Mini-automi per i 3 template #TODO: PROVA DECLARE4PY potrei calcolare la fitness direttamente sulla realizzazione
# ------------------------------------------------------------------

# End automaton  
class End:
    def __init__(self, alpha):         # alpha = list of transition ids for the End template in the original decspec
        #print(alpha)                  
        self.X = set(alpha)            # [ALPHABETH] set of transition ids that are considered as End 
        #print("End X:", self.X)
        self.after_x   = False         # [STATE] True if at least one transition in X has been seen, False otherwise
        self.bad_tail  = False         # [STATE] True if the trace ends with a transition in X, False otherwise @TODO CHECK DA FARE

        self.msg = []                  # buffer violazioni
        self.pos = -1                  # position counter (0-based)

    def step(self, t):                 # Visit every element in the realization    
        #print("Step:", t)
        self.pos += 1                  # avanza indice

        if t in self.X:                # if elem is in X
            self.after_x  = True       # [TRANSITION] mark as seen
            self.bad_tail = False      # if we see an X, we reset the bad_tail flag
        else:                                                                                # simbolo diverso da X
            if self.after_x:           # …e arriva DOPO un X
                if not self.bad_tail:  # registra solo la prima volta
                    labs = ",".join(id2lab(x) for x in self.X)
                    ids  = ",".join(self.X)
                    self.msg.append(
                        f"[pos {self.pos}] End({labs}) violated (id {ids})"
                    )
                self.bad_tail = True   # flag violazione coda

    def result(self):                       # check post-trace
        # se bad_tail True, il messaggio è già stato aggiunto
        if not self.after_x:           # se mai visto X
            labs = ",".join(id2lab(x) for x in self.X)  
            ids  = ",".join(self.X)
            self.msg.append(
                f"[pos END] End({labs}) missing (id {ids})"
            )
        # se after_x True ma bad_tail True, il messaggio è già stato aggiunto
        return len(self.msg), self.msg


# AtMost1 automaton
class AtMost1:
    def __init__(self, alpha):
        #print(alpha)
        self.X = set(alpha)             # [ALPHABETH] set of transition ids that are considered as AtMost1
        self.count = 0
        self.msg = []
        self.pos = -1                      # position counter (0-based)

    def step(self, t):
        #print("Step:", t)
        self.pos += 1                      # avanza indice 0-based
        if t in self.X:
            self.count += 1       # count the number of transitions in X seen   
            if self.count > 1:            # if more than one transition in X has been seen → violation
                labs = ",".join(id2lab(x) for x in self.X)
                ids  = ",".join(self.X)
                self.msg.append(
                    f"[pos {self.pos}] AtMost1({labs}) repeated (id {ids})"
                )

    def result(self):
        return len(self.msg), self.msg


# AlternatePrecedence automaton
class AltPrecedence:
    def __init__(self, Target, Activator): # Target and Activator transition ids lists
        #print(Target, Activator)
        self.X, self.Y = set(Target), set(Activator) # [ALPHABETH] set of transition ids that are considered as Target and Activator
        self.waiting_target = True # [STATE]: True = sto aspettando un X che chiuda l’ultimo Y visto
        self.msg = []                # buffer violazioni
        self.pos = -1                 # position counter (0-based)

    def step(self, t):
        self.pos += 1                    # avanza indice 0-based

        if self.waiting_target:                       # stato OPEN  (nessun Y aperto)
            if t in self.Y:                           # Y apre una nuova coppia
                # RElabeling
                labsX = ",".join(sorted(id2lab(x) for x in self.X)) 
                labsY = ",".join(sorted(id2lab(y) for y in self.Y))
                idsY  = ",".join(sorted(self.Y))
                self.msg.append(                           
                    f"[pos {self.pos}] AltPrec({{{labsX}}},{{{labsY}}}): "
                    f"violated in (id {idsY})"
                )
            elif t in self.X:                         # visto X
                self.waiting_target = False
        else:                                         # aspetto Y per chiudere
            if t in self.Y:                           # Y chiude la coppia
                self.waiting_target = True

    def result(self):
        return len(self.msg), self.msg




# ------------------------------------------------------------------
# Costruzione dei vincoli a partire dalla specifica sulla base degli automi definiti sopra
# ------------------------------------------------------------------

def build_constraints(spec_json):
    constraints = []
    for c in spec_json["constraints"]:
        tmpl, parameter = c["template"], c["parameters"]

        if tmpl == "End":
            constraints.append(End(*parameter)) # append l'oggetto End sui parameters della specifica del mago

        elif tmpl == "Atmost1":
            constraints.append(AtMost1(*parameter))

        elif tmpl == "AlternatePrecedence":
            constraints.append(AltPrecedence(parameter[0], parameter[1]))
    return constraints

CONSTRAINTS = build_constraints(model_json)
#print(type(CONSTRAINTS))
#print(CONSTRAINTS)


# ------------------------------------------------------------------
# Cost function for each realization
# ------------------------------------------------------------------

def declare_cost(realization):
    constraints = copy.deepcopy(CONSTRAINTS)   # deepcopy for cleaning automata for each realization

    for t in realization:
        for c in constraints:
            c.step(t)   # passo la transizione della realization al vincolo costruito come automa

    total = 0
    details = []                                
    for c in constraints:
        viol, msgs = c.result()                 
        total += viol
        details.extend(msgs)

    return total, details                       


#TODO: QUI SE VOGLIAMO QUALCHE EURISTICA
# ------------------------------------------------------------------
# Ricerca brute-force cross product

choices = [L_inv[label] for label in input_trace] # lista di alternative/posizione
best_cost, best_real, best_detail = math.inf, None, None

for combo in product(*choices): # combo sono le realizzazioni possibili
    print("Combo:", combo)
    cost, detail = declare_cost(combo)
    if cost < best_cost:
        best_cost, best_real, best_detail = cost, combo, detail



print("****************************************************************************")
print("INPUT TRACE LABELS:", input_trace)
print("REALIZATION (ID):", best_real)
print("MINIMUM COST (constraint violation counter):", best_cost)
print("VIOLATIONS:")
for d in best_detail:
    print("  -", d)




exit()










# VERSIONE SENZA DETTAGLI SU VIOLAZIONI

#TODO: DA FARE TEST DECLARE4PY 
# ------------------------------------------------------------------
# Mini-automi per i 3 template 

# End automaton
class End:
    def __init__(self, alpha):       # alpha = list of transition ids for the End template in the original decspec
        #print(alpha)       
        self.X = set(alpha)          # [ALPHABETH] set of transition ids that are considered as End 
        #print("End X:", self.X)
        self.seen = False            # [STATE] True if at least one transition in X has been seen, False otherwise
        
    
    def step(self, t):               # Visit every element in the realization  
        #print("Step:", t)
        if t in self.X:              # if elem is in X
            self.seen = True         # [TRANSITION] mark as seen
    
    def result(self):                # check post-trace
        return 0 if self.seen else 1 


# AtMost1 automaton
class AtMost1: 
    def __init__(self, alpha):
        #print(alpha)
        self.X = set(alpha); self.count = 0; self.viol = 0 # [ALPHABETH] set of transition ids that are considered as AtMost1

    def step(self, t):
        #print("Step:", t)
        if t in self.X:
            self.count += 1 # count the number of transitions in X seen
            if self.count > 1: # if more than one transition in X has been seen --> violation
                self.viol += 1  # increment violation counter

    def result(self):
        return self.viol # [OUTPUT] return the violation counter


# AlternatePrecedence automaton
class AltPrecedence:                

    def __init__(self, Target, Activator): # Target and Activator transition ids lists
        #print(Target, Activator)
        self.X, self.Y = set(Target), set(Activator)  # [ALPHABETH] set of transition ids that are considered as Target and Activator
        
        # [STATE]: True = sto aspettando un X che chiuda l’ultimo Y visto
        #        False = sto aspettando un nuovo Y
        self.waiting_target = True; self.viol = 0 # counter for violations
        
    def step(self, t):
        if not self.waiting_target:          # stato OPEN  (nessun Y aperto)
            if t in self.X:                  # X senza Y → violazione
                self.viol += 1
            elif t in self.Y:                # Y apre una nuova coppia
                self.waiting_target = True

        else:                                # stato WAIT (aspetto un X)
            if t in self.Y:                  # nuovo Y prima di X → violazione
                self.viol += 1               # conto la violazione...
                # ...e il nuovo Y diventa quello "aperto"
                # (resto in waiting_target = True)
            elif t in self.X:                # X chiude la coppia
                self.waiting_target = False  # torno in stato OPEN


    def result(self):
        return self.viol

# ------------------------------------------------------------------
# Costruzione dei vincoli a partire dalla specifica sulla base degli automi definiti sopra

def build_constraints(spec_json):
    """automini a partire dalla specifica"""

    constraints = []
    for c in spec_json["constraints"]:
        tmpl, parameter = c["template"], c["parameters"]

        if tmpl == "End":
            constraints.append(End(*parameter)) # append l'oggetto End sui parameters della specifica del mago

        elif tmpl == "Atmost1":
            constraints.append(AtMost1(*parameter))

        elif tmpl == "AlternatePrecedence":
            constraints.append(AltPrecedence(parameter[0], parameter[1]))
    
    return constraints



CONSTRAINTS = build_constraints(model_json)
#print(type(CONSTRAINTS))
#print(CONSTRAINTS)


# ------------------------------------------------------------------
# Cost function for each realization

def declare_cost(realization):

    constraints = copy.deepcopy(CONSTRAINTS)       # deepcopy for cleaning automata for each realization

    for t in realization:
        for c in constraints: 
            c.step(t)  # passo la transizione della realization al vincolo costruito come automa

    return sum(c.result() for c in constraints)  # somma dei risultati di tutti i vincoli




#TODO: QUI SE VOGLIAMO QUALCHE EURISTICA
# ------------------------------------------------------------------
# Ricerca brute-force cross product, 

choices = [L_inv[label] for label in input_trace]   # lista di alternative/posizione
best_cost, best_real = math.inf, None

for combo in product(*choices): # combo sono le realizzazioni possibili
    cost = declare_cost(combo)
    if cost < best_cost:
        best_cost, best_real = cost, combo

print("****************************************************************************")
print("Input Trace Lables : ", input_trace)
print("REALIZATION (id):", best_real)
print("MINIMUM COST (constraint violation counter):", best_cost)