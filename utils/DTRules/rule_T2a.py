import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

# RULE T2a - XOR SPLIT
# Task t1 is replaced by two conditional tasks t2 and t3. 
# This transformation rule corresponds to the specialization of a task (e.g. handle order) into two more specialized tasks (e.g. handle small order and handle large order).

# Random activity name generator
def generate_random_activity_name():
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{random_suffix}"

# T2a
def xor_split_transition_t3a(petri_net, target_transition=None, t2_name=None, t3_name=None):  
    
     # seleziono t1
    if target_transition is None:  #TODO SELEZIONE DELLA TRANSITION SU CUI APPLICARE LA TRASFORMAZIONE, VEDI MAIN-TEST (UTILIZZO UN A TRS PIVOT)
        target_transition = random.choice(list(petri_net.transitions))
    elif isinstance(target_transition, str):  # Se target_transition è una stringa (nome della transizione)
        target_transition = next((t for t in petri_net.transitions if t.name == target_transition), None)
        # if target_transition is None:
        #     raise ValueError
    
    incoming_places = [arc.source for arc in target_transition.in_arcs]
    outgoing_places = [arc.target for arc in target_transition.out_arcs]
    
    for arc in list(target_transition.in_arcs) + list(target_transition.out_arcs):
        utils.remove_arc(petri_net, arc)
    petri_net.transitions.remove(target_transition)
    
    # t2 e t3
    if t2_name is None:
        t2_name = generate_random_activity_name()   #TODO: CONTROLLA IL CICLO IN MAIN

    if t3_name is None:
        t3_name = generate_random_activity_name()   #TODO: CONTROLLA IL CICLO IN MAIN
    
    t2 = PetriNet.Transition(t2_name, label=t2_name)
    t3 = PetriNet.Transition(t3_name, label=t3_name)
    petri_net.transitions.add(t2)
    petri_net.transitions.add(t3)
    
    for place in incoming_places: #TODO   QUI FORSE DOVREI MARCARE I PLACE ESTREMI PER LIMITARE LO SPAZIO DELLA MIA ESPANSIONE
        utils.add_arc_from_to(place, t2, petri_net)
        utils.add_arc_from_to(place, t3, petri_net)
    
    for place in outgoing_places:
        utils.add_arc_from_to(t2, place, petri_net)
        utils.add_arc_from_to(t3, place, petri_net)
    
    #print(f"Transition {target_transition.name} replaced by {t2_name} and {t3_name}.")
    return petri_net