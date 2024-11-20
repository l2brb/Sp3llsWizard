import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter


# RULE T3a - AND SPLIT
# Task t1 is replaced by two parallel tasks t2 and t3. 
# The effect of the execution of t2 and t3 is identical to the effect of the execution of t1. The transitions c1 and c2 represent control activities to fork and join two parallel threads.


def generate_random_name():
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{random_suffix}"

# T3a
def and_split_transition_t3a(petri_net, target_transition=None, t2_name=None, t3_name=None):

   # seleziono t1
    if target_transition is None:  #TODO SELEZIONE DELLA TRANSITION SU CUI APPLICARE LA TRASFORMAZIONE, VEDI MAIN-TEST (UTILIZZO UN A TRS PIVOT)
        target_transition = random.choice(list(petri_net.transitions))
    elif isinstance(target_transition, str):  # Se target_transition è una stringa (nome della transizione)
        target_transition = next((t for t in petri_net.transitions if t.name == target_transition), None)
        # if target_transition is None:
        #     raise ValueError
    
    incoming_places = [arc.source for arc in target_transition.in_arcs]
    outgoing_places = [arc.target for arc in target_transition.out_arcs]
    

    # c1 e c2 #TODO: HOUN PROBLEMA QUI SE REITERO PERCHE I PLACES CAMBIANO

    # Find the transition that precedes t1 (c1)
    c1 = next((arc.source for place in incoming_places for arc in place.in_arcs if isinstance(arc.source, PetriNet.Transition)), None)

    # Find the transition that follows t1 (c2)
    c2 = next((arc.target for place in outgoing_places for arc in place.out_arcs if isinstance(arc.target, PetriNet.Transition)), None)


    # c1 = next((arc.source for arc in incoming_places[0].in_arcs if isinstance(arc.source, PetriNet.Transition)), None) 
    # c2 = next((arc.target for arc in outgoing_places[0].out_arcs if isinstance(arc.target, PetriNet.Transition)), None)

    if not c1 or not c2:
        raise ValueError

    # for arc in list(target_transition.in_arcs) + list(target_transition.out_arcs):
    #     utils.remove_arc(petri_net, arc)
    # petri_net.transitions.remove(target_transition)
    
    # t2 e t3
    if t2_name is None:
        t2_name = generate_random_name()   #TODO: CONTROLLA IL CICLO IN MAIN

    if t3_name is None:
        t3_name = generate_random_name()   #TODO: CONTROLLA IL CICLO IN MAIN
    
    t2 = target_transition
    t3 = PetriNet.Transition(t3_name, label=t3_name)
    petri_net.transitions.add(t2)
    petri_net.transitions.add(t3)
    
    # place_c1_t2 = PetriNet.Place(generate_random_name())
    place_c1_t3 = PetriNet.Place(generate_random_name())
    # place_t2_c2 = PetriNet.Place(generate_random_name())
    place_t3_c2 = PetriNet.Place(generate_random_name())
    # petri_net.places.add(place_c1_t2)
    petri_net.places.add(place_c1_t3)
    # petri_net.places.add(place_t2_c2)
    petri_net.places.add(place_t3_c2)
    
   
    # utils.add_arc_from_to(c1, place_c1_t2, petri_net)
    utils.add_arc_from_to(c1, place_c1_t3, petri_net)
    # utils.add_arc_from_to(place_c1_t2, t2, petri_net)
    utils.add_arc_from_to(place_c1_t3, t3, petri_net)
    # utils.add_arc_from_to(t2, place_t2_c2, petri_net)
    utils.add_arc_from_to(t3, place_t3_c2, petri_net) 
    # utils.add_arc_from_to(place_t2_c2, c2, petri_net)
    utils.add_arc_from_to(place_t3_c2, c2, petri_net)


    #print(f"Transition {target_transition.name} replaced by parallel tasks {t2_name} and {t3_name} with control transitions {c1_name} and {c2_name}.")
    return petri_net
