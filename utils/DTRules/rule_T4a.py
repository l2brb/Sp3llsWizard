import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter


# RULE T4a - LOOP
# Task t1 is replaced by an iteration of task t2.
# The execution of task t1 (e.g. type letter) corresponds to zero or more executions of task t2 (e.g.type sentence). 
# The transitions c1 and c2 represent control activities that mark the begin and end of a sequence of ‘t2-tasks’.


#Random activity name generator
def generate_random_activity_name():
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{random_suffix}"

# T4a
def loop_transition_t4a(petri_net):
    
    # seleziono t1
    if target_transition is None:  #TODO SELEZIONE DELLA TRANSITION SU CUI APPLICARE LA TRASFORMAZIONE, VEDI MAIN-TEST (UTILIZZO UNA TRS PIVOT)
        target_transition = random.choice(list(petri_net.transitions))
    elif isinstance(target_transition, str):  # Se target_transition è una stringa (nome della transizione)
        target_transition = next((t for t in petri_net.transitions if t.name == target_transition), None)
        if target_transition is None:
            raise ValueError
    

    
    incoming_places = [arc.source for arc in target_transition.in_arcs]
    outgoing_places = [arc.target for arc in target_transition.out_arcs]
    
    for arc in list(target_transition.in_arcs) + list(target_transition.out_arcs):
        utils.remove_arc(petri_net, arc)
    petri_net.transitions.remove(target_transition)
    
    # c1 e c2
    c1_name = generate_random_activity_name()
    c2_name = generate_random_activity_name()
    c1 = PetriNet.Transition(c1_name, label=c1_name)
    c2 = PetriNet.Transition(c2_name, label=c2_name)
    petri_net.transitions.add(c1)
    petri_net.transitions.add(c2)
    
    # Loop in t2
    t2_name = generate_random_activity_name()
    t2 = PetriNet.Transition(t2_name, label=t2_name)
    petri_net.transitions.add(t2)


    place_c1_t2_t3 = PetriNet.Place(generate_random_activity_name())
    petri_net.places.add(place_c1_t2_t3)
    
   
    for place in incoming_places:
        utils.add_arc_from_to(place, c1, petri_net)
    

    utils.add_arc_from_to(c1, place_c1_t2_t3, petri_net)
    utils.add_arc_from_to(t2, place_c1_t2_t3, petri_net)
    utils.add_arc_from_to(place_c1_t2_t3, t2, petri_net)
    utils.add_arc_from_to(place_c1_t2_t3, c2, petri_net)
    

    for place in outgoing_places:
        utils.add_arc_from_to(c2, place, petri_net)
    
    #print(f"Transition {target_transition.name} replaced by parallel tasks {t2_name} and {t3_name} with control transitions {c1_name} and {c2_name}.")
    return petri_net

