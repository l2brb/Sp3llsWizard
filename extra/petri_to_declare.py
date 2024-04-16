import pm4py
import pandas as pd


# Read XES
event_log = pm4py.read_xes(
    '/Users/luca/Documents/^main/TEExProcessMining/procedural_to_declarative/petri_test/bpic12/BPI_Challenge_2012.xes'
    )

# Discover the Petri net
net, im, fm = pm4py.discover_petri_net_heuristics(
    event_log)
print(net)


# Visualize the Petri net
# pm4py.view_petri_net(net, im, fm, format='pdf')
# pm4py.save_vis_petri_net(net, im, fm, file_path='/Users/luca/Documents/^main/TEExProcessMining/models/petri.pdf')

# Discover the BPMN
#bpmn_graph = pm4py.discover_bpmn_inductive(
    #event_log)
# Visualize the bpmn
#pm4py.view_bpmn(bpmn_graph, format='pdf')
#pm4py.save_vis_bpmn(bpmn_graph, file_path='/Users/luca/Documents/^main/TEExProcessMining/models/bpmn.pdf')

# Discover the Process Tree
process_tree = pm4py.discover_process_tree_inductive(
    event_log)
# Visualize the Process Tree
pm4py.view_process_tree(process_tree, format='pdf')
#pm4py.save_vis_process_tree(process_tree, file_path='/Users/luca/Documents/^main/TEExProcessMining/models/tree.pdf')



########################################################################### WHAT'S INSIDE? ##########################################################################
#Place
for plc in net.places:
    print((plc))
print("######################################")
#Transition
for trs in net.transitions:
    print((trs))
print("######################################")
#Arc
for arc in net.arcs:
    print((arc))
print("######################################")


########################################################################### DICT ##########################################################################




# Converto gli archi della petri net in un dizionario
arc_dict = {str(arc.source): str(arc.target) for arc in net.arcs}
print(arc_dict)

# Converto le transizioni della petri net in una lista
trs_list = [str(trs.name) for trs in net.transitions]
# print(trs_list)
# Converto i places della petri net in una lista
plc_list = [str(plc.name) for plc in net.places]
# print(plc_list)

trs_list_by_arcs = [(arc.source.name, arc.target.name) for arc in net.arcs]
print(trs_list_by_arcs)
#Source
source_list_by_arcs = [(arc.source) for arc in net.arcs]
print(source_list_by_arcs)
#Target
target_list_by_arcs = [(arc.target) for arc in net.arcs]
print(target_list_by_arcs)

###################### EXISTANCE ######################

# Check_Init
# A is the first to occur
def check_init(arc_dict, A):
    # Controlliamo se esiste un arco da source0 all'attività A
    for elem in dict(arc_dict):
        if elem == 'source0' and dict(arc_dict)[elem] == A:
            return 1
    return 0

init_check = check_init(arc_dict)

# Check_End
# A is the last to occur
def check_end(arc_dict, A):
    # Controlliamo se esiste un arco da source0 all'attività A
    for elem in dict(arc_dict):
        if elem == 'source0' and dict(arc_dict)[elem] == A:
            return 1
    return 0

init_check = check_init(arc_dict)



###################### RELATION ######################


"""# Check_AlternatePrecedence
def check_alternate_precedence(net, A, B):
    # Ottieni la sequenza di transizioni dalla rete
    # Inizializza un contatore per A
    count_A = 0
    # Scorri la sequenza di transizioni
    for arc in net.arcs:
        # Se la transizione è A, incrementa il contatore
        if arc.target == A:
            count_A += 1
        # Se la transizione è B
        elif arc.source == B:
            # Se il contatore per A è zero, il vincolo non è rispettato
            if count_A == 0:
                return False
            # Altrimenti, decrementa il contatore per A
            else:
                count_A -= 1
    return True"""

# Check_AlternatePrecedence
# If A occurs then B occurs afterwards, and no other a recurs in between

def check_alternate_precedence(arc_dict, A, B):
    last_activity = None
    for arc in net.arcs:
        if arc.target == B:
            # Se l'ultima attività non era A, il vincolo non è rispettato
            if last_activity != A:
                return False
        # Se la transizione è A, registrala come l'ultima attività
        elif arc.source == A:
            last_activity = A
        return True

for i in range(len(trs_list)):
    for j in range(i+1, len(trs_list)):
        A = trs_list[i]
        B = trs_list[j]
        result = check_alternate_precedence(arc_dict, A, B)
        print(f"Alternate Precedence check for {A} and {B}: {result}")




# Check_AlternateResponse
# Each time B occurs, it is preceded by A and no other B can recur in between
def check_AlternateResponse(arc_dict, A):
    # Controlliamo se esiste un arco da source0 all'attività A
    for elem in dict(arc_dict):
        if elem == 'source0' and dict(arc_dict)[elem] == A:
            return 1
    return 0

init_check = check_AlternateResponse(arc_dict)




exit()



"""# PETRI NET TO DICT
def petri_to_dict(petri_net):
    petri_dict = {}
    petri_dict['places'] = [str(place) for place in petri_net.places]
    petri_dict['transitions'] = [str(transition) for transition in petri_net.transitions]
    petri_dict['arcs'] = [(str(arc.source), str(arc.target)) for arc in petri_net.arcs]
    return petri_dict

# Uso della funzione
petri_dict = petri_to_dict(net[0])

print(petri_dict['arcs'])"""


net = pm4py.read_pnml(
     "procedural_to_declarative/petri_pharma.pnml"
     )

"""(places: [ pre_Produce drug in laboratory, pre_Ship drug, sink0, source0 ]
transitions: [ (Produce drug in laboratory, 'Produce drug in laboratory'), (Receive drugs order from hospital, 'Receive drugs order from hospital'), (Ship drug, 'Ship drug') ]
arcs: [ (Produce drug in laboratory, 'Produce drug in laboratory')->pre_Ship drug, (Receive drugs order from hospital, 'Receive drugs order from hospital')->pre_Produce drug in laboratory, (Ship drug, 'Ship drug')->sink0, pre_Produce drug in laboratory->(Produce drug in laboratory, 'Produce drug in laboratory'), pre_Ship drug->(Ship drug, 'Ship drug'), source0->(Receive drugs order from hospital, 'Receive drugs order from hospital') ], ['source0:1'], ['sink0:1'])"""

"""(places: [ pre_Produce drug in laboratory, pre_Ship drug, sink0, source0 ]
transitions: [ (Produce drug in laboratory, 'Produce drug in laboratory'), (Receive drugs order from hospital, 'Receive drugs order from hospital'), (Ship drug, 'Ship drug') ]
arcs: [ (Produce drug in laboratory, 'Produce drug in laboratory')->pre_Ship drug, (Receive drugs order from hospital, 'Receive drugs order from hospital')->pre_Produce drug in laboratory, (Ship drug, 'Ship drug')->sink0, pre_Produce drug in laboratory->(Produce drug in laboratory, 'Produce drug in laboratory'), pre_Ship drug->(Ship drug, 'Ship drug'), source0->(Receive drugs order from hospital, 'Receive drugs order from hospital') ], ['source0:1'], ['sink0:1'])"""
print(tuple(net))
exit()

net = (
    ['pre_Produce drug in laboratory', 'pre_Ship drug', 'sink0', 'source0'],
    [('Produce drug in laboratory', 'Produce drug in laboratory'), ('Receive drugs order from hospital', 'Receive drugs order from hospital'), ('Ship drug', 'Ship drug')],
    [(('Produce drug in laboratory', 'Produce drug in laboratory'), 'pre_Ship drug'), (('Receive drugs order from hospital', 'Receive drugs order from hospital'), 'pre_Produce drug in laboratory'), (('Ship drug', 'Ship drug'), 'sink0'), ('pre_Produce drug in laboratory', ('Produce drug in laboratory', 'Produce drug in laboratory')), ('pre_Ship drug', ('Ship drug', 'Ship drug')), ('source0', ('Receive drugs order from hospital', 'Receive drugs order from hospital'))],
    ['source0:1'],
    ['sink0:1']
)


# Init

def check_init(net, A):
    # Estraiamo gli archi dalla rete
    arcs = net[2]
    # Controlliamo se esiste un arco da source0 all'attività A
    for arc in arcs:
        if arc[0][0] == 'source0' and arc[1] == A:
            return 1
    return 0

# Esempio di utilizzo

print(check_init(net, 'Receive drugs order from hospital'))  # Output: 1

exit()


def check_precedence(log, A, B):
    if B in log and A not in log[:log.index(B)]:
        return 0
    return 1

def check_response(log, A, B):
    if A in log and B not in log[log.index(A):]:
        return 0
    return 1

def check_chain_precedence(log, A, B):
    indices = [i for i, x in enumerate(log) if x == B]
    for index in indices:
        if index == 0 or log[index - 1] != A:
            return 0
    return 1

def check_chain_response(log, A, B):
    indices = [i for i, x in enumerate(log) if x == A]
    for index in indices:
        if index == len(log) - 1 or log[index + 1] != B:
            return 0
    return 1

def check_at_most_one(log, A):
    if log.count(A) > 1:
        return 0
    return 1

def check_at_least_one(log, A):
    if log.count(A) < 1:
        return 0
    return 1

def check_init(log, A):
    if log[0] != A:
        return 0
    return 1

def check_absence(log, A):
    if A in log:
        return 0
    return 1

def check_end(log, A):
    if log[-1] != A:
        return 0
    return 1

# Esempio di utilizzo
log = ['Receive drugs order from hospital', 'Produce drug in laboratory', 'Ship drug']
data = {
    'Precedence': check_precedence(log, 'Receive drugs order from hospital', 'Produce drug in laboratory'),
    'Response': check_response(log, 'Produce drug in laboratory', 'Ship drug'),
    'ChainPrecedence': check_chain_precedence(log, 'Receive drugs order from hospital', 'Produce drug in laboratory'),
    'ChainResponse': check_chain_response(log, 'Produce drug in laboratory', 'Ship drug'),
    'AtMostOne': check_at_most_one(log, 'Ship drug'),
    'AtLeastOne': check_at_least_one(log, 'Receive drugs order from hospital'),
    'Init': check_init(log, 'Receive drugs order from hospital'),
    'Absence': check_absence(log, 'Receive drugs order from hospital'),
    'End': check_end(log, 'Ship drug')
}
df = pd.DataFrame(data, index=[0])
print(df)

exit()





first = net[0]

place_names = []
for place in first.places:
    place_names.append(place.name)   

transitions_names = []
for transitions in first.transitions:
    transitions_names.append(transitions.name)   

arcs_source = []
for arcs in first.arcs:
    arcs_source.append(arcs.source)

arcs_target = []
for arcs in first.arcs:
    arcs_target.append(arcs.target)

print(place_names)
print(transitions_names)
print(arcs_source)
print(arcs_target)
exit()

"""second = net[1]
print(second)
exit()"""
"""third = net[2]
print(third)
exit()"""


# Visualize the Petri net
pm4py.save_vis_petri_net(net, im, fm, file_path='/Users/luca/Documents/^main/TEExProcessMining/procedural_to_declarative/petri_pharma.pdf')
# Visualize the BPMN
bpmn_graph = pm4py.convert_to_bpmn(net, im, fm)
pm4py.view_bpmn(bpmn_graph, format='pdf')


exit()







