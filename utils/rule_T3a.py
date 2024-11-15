import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter


# RULE T3a
# Task t1 is replaced by two parallel tasks t2 and t3. 
# The effect of the execution of t2 and t3 is identical to the effect of the execution of t1. The transitions c1 and c2 represent control activities to fork and join two parallel threads.


def generate_random_activity_name():
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{random_suffix}"

# T3a
def replace_random_transition_t3a(petri_net):
    
    target_transition = random.choice(list(petri_net.transitions))
    
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
    
    # t2 e t3
    t2_name = generate_random_activity_name()
    t3_name = generate_random_activity_name()
    t2 = PetriNet.Transition(t2_name, label=t2_name)
    t3 = PetriNet.Transition(t3_name, label=t3_name)
    petri_net.transitions.add(t2)
    petri_net.transitions.add(t3)
    
    place_c1_t2 = PetriNet.Place(generate_random_activity_name())
    place_c1_t3 = PetriNet.Place(generate_random_activity_name())
    place_t2_c2 = PetriNet.Place(generate_random_activity_name())
    place_t3_c2 = PetriNet.Place(generate_random_activity_name())
    petri_net.places.add(place_c1_t2)
    petri_net.places.add(place_c1_t3)
    petri_net.places.add(place_t2_c2)
    petri_net.places.add(place_t3_c2)
    
   
    for place in incoming_places:
        utils.add_arc_from_to(place, c1, petri_net)
    

    utils.add_arc_from_to(c1, place_c1_t2, petri_net)
    utils.add_arc_from_to(c1, place_c1_t3, petri_net)
    utils.add_arc_from_to(place_c1_t2, t2, petri_net)
    utils.add_arc_from_to(place_c1_t3, t3, petri_net)
    utils.add_arc_from_to(t2, place_t2_c2, petri_net)
    utils.add_arc_from_to(t3, place_t3_c2, petri_net) 
    utils.add_arc_from_to(place_t2_c2, c2, petri_net)
    utils.add_arc_from_to(place_t3_c2, c2, petri_net)

    for place in outgoing_places:
        utils.add_arc_from_to(c2, place, petri_net)
    
    #print(f"Transition {target_transition.name} replaced by parallel tasks {t2_name} and {t3_name} with control transitions {c1_name} and {c2_name}.")
    return petri_net

########################################################################################### EXECUTION

intervals = [1, 2, 3, 4, 5, 6, 7]  #TODO: SCALA DA RIVEDERE, DEVO DECIDERE COME APPLICARE LA REGOLA


def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/utils/simple-wn.pnml"
    
    petri_net, initial_marking, final_marking = pnml_importer.apply(pnml_file_path)

    for num_activities in intervals:
        updated_petri_net = replace_random_transition_t3a(petri_net)

        output_file_path = f"/home/l2brb/main/DECpietro/utils/Trules/T3a/T3a_augmented_{num_activities}.pnml"
        if updated_petri_net:
            pnml_exporter.apply(updated_petri_net, initial_marking, output_file_path, final_marking=final_marking)
            print(f"Updated WN with {num_activities + 1} activities exported to {output_file_path}")

if __name__ == "__main__":
    main()