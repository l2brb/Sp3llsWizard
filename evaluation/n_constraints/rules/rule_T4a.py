import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils

# RULE T4a - LOOP
# Task t1 is replaced by an iteration of task t2.
# The execution of task t1 (e.g. type letter) corresponds to zero or more executions of task t2 (e.g.type sentence). 
# The transitions c1 and c2 represent control activities that mark the begin and end of a sequence of ‘t2-tasks’.


# Random activity name generator
def generate_random_activity_name():
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{random_suffix}"

# T4a
def loop_transition_t4a(petri_net):
    # Trova p1 e p2
    p1 = next((p for p in petri_net.places if p.name == 'p1'), None)
    p2 = next((p for p in petri_net.places if p.name == 'p2'), None)

    if not p1 or not p2:
        raise ValueError("p1 or p2 not found")

    # Trovo la transizione dopo p1
    post_p1_transition = next((arc.target for arc in p1.out_arcs), None)

    # Trovo la transizione prima di p2
    pre_p2_transition = next((arc.source for arc in p2.in_arcs), None)

    # Rimuovo l'arco tra p1 e post_p1
    for arc in list(p1.out_arcs):
        if arc.target == post_p1_transition:
            utils.remove_arc(petri_net, arc)

    # Rimuovi gli archi tra pre_p2 e p2
    for arc in list(p2.in_arcs):
        if arc.source == pre_p2_transition:
            utils.remove_arc(petri_net, arc)


    # POST P1
    new_transition_after_p1 = PetriNet.Transition(generate_random_activity_name(), label=generate_random_activity_name())
    new_place_after_p1 = PetriNet.Place(generate_random_activity_name())

    petri_net.transitions.add(new_transition_after_p1)
    petri_net.places.add(new_place_after_p1)

    utils.add_arc_from_to(p1, new_transition_after_p1, petri_net)
    utils.add_arc_from_to(new_transition_after_p1, new_place_after_p1, petri_net)
    utils.add_arc_from_to(new_place_after_p1, post_p1_transition, petri_net)

    # PRE P2
    new_place_before_p2 = PetriNet.Place(generate_random_activity_name())
    new_transition_before_p2 = PetriNet.Transition(generate_random_activity_name(), label=generate_random_activity_name())
    petri_net.places.add(new_place_before_p2)
    petri_net.transitions.add(new_transition_before_p2)

    utils.add_arc_from_to(pre_p2_transition, new_place_before_p2, petri_net)
    utils.add_arc_from_to(new_place_before_p2, new_transition_before_p2, petri_net)
    utils.add_arc_from_to(new_transition_before_p2, p2, petri_net)


    # LOOP
    intermediate_trs = PetriNet.Transition(generate_random_activity_name(), label=generate_random_activity_name())
    petri_net.transitions.add(intermediate_trs)
    
    utils.add_arc_from_to(new_place_before_p2, intermediate_trs, petri_net)
    utils.add_arc_from_to(intermediate_trs, new_place_after_p1, petri_net)



    return petri_net
