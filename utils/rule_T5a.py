import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter


# RULE T5a
# Two consecutive tasks are replaced by two parallel tasks. 
# The application of transformation rule T5a corresponds to the application of T1b followed by the application of T3a


#Random activity name generator
def generate_random_activity_name():
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{random_suffix}"


def replace_transition_t5a(petri_net):

    target_transition1 = random.choice(list(petri_net.transitions)) #TODO   qui ho la saelezione casuale, ma devo decidere come fare nei test
    
   
    target_transition2 = None
    for arc in target_transition1.out_arcs:
        if isinstance(arc.target, PetriNet.Place):
            target_transition2 = next((arc2.target for arc2 in arc.target.out_arcs if isinstance(arc2.target, PetriNet.Transition)), None)
            if target_transition2:
                break
    
    if not target_transition2:
        print("No consecutive transition")
        return
    
 
    incoming_places = [arc.source for arc in target_transition1.in_arcs]
    outgoing_places = [arc.target for arc in target_transition2.out_arcs]

    for arc in list(target_transition1.in_arcs) + list(target_transition1.out_arcs):
        utils.remove_arc(petri_net, arc)
    for arc in list(target_transition2.in_arcs) + list(target_transition2.out_arcs):
        utils.remove_arc(petri_net, arc)
    petri_net.transitions.remove(target_transition1)
    petri_net.transitions.remove(target_transition2)
    
    
    # c1 e c2
    c1_name = generate_random_activity_name()
    c2_name = generate_random_activity_name()
    c1 = PetriNet.Transition(c1_name, label=c1_name)
    c2 = PetriNet.Transition(c2_name, label=c2_name)
    petri_net.transitions.add(c1)
    petri_net.transitions.add(c2)
    
    # t2 e t3
    t2 = PetriNet.Transition(target_transition1.name, label=target_transition1.label)
    t3 = PetriNet.Transition(target_transition2.name, label=target_transition2.label)
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
    
    print(f"Transitions {target_transition1.name} and {target_transition2.name} replaced by parallel tasks {t2.name} and {t3.name} with control transitions {c1_name} and {c2_name}.")
    return petri_net

########################################################################################### EXECUTION

log_intervals = [1, 2, 3, 4, 5, 6, 7]  #TODO: SCALA DA RIVEDERE, DEVO DECIDERE COME APPLICARE LA REGOLA

def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/utils/Trules/T1a/T1a_augmented_1.pnml"
    
    petri_net, initial_marking, final_marking = pnml_importer.apply(pnml_file_path)

    for num_activities in log_intervals:
        updated_petri_net = replace_transition_t5a(petri_net)

        output_file_path = f"/home/l2brb/main/DECpietro/utils/Trules/T5a/T5a_augmented_{num_activities}.pnml"
        if updated_petri_net:
            pnml_exporter.apply(updated_petri_net, initial_marking, output_file_path, final_marking=final_marking)
            print(f"Updated Petri net with {num_activities + 1} activities exported to {output_file_path}")

if __name__ == "__main__":
    main()