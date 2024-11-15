import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter


def generate_random_activity_name():
    random_suffix = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
    return f"Activity_{random_suffix}"


def add_activities(petri_net, num_activities, target_place_id):
    target_place = next((place for place in petri_net.places if place.name == target_place_id), None)
    if not target_place:
        print(f"Place with id {target_place_id} not found.")
        return
    
    original_target_place = target_place  
    next_transition = next((arc.target for arc in original_target_place.out_arcs), None)
    
    if next_transition:
  
        arc_to_remove = next((arc for arc in original_target_place.out_arcs if arc.target == next_transition), None)
        if arc_to_remove:
            utils.remove_arc(petri_net, arc_to_remove)
    else:
        print("No transition found following the target place to reconnect the flow.")
    
  
    new_place = PetriNet.Place(f"p_{generate_random_activity_name()}")
    petri_net.places.add(new_place)

    for _ in range(num_activities):
        activity_name = generate_random_activity_name()
        new_transition = PetriNet.Transition(activity_name, label=activity_name)
        petri_net.transitions.add(new_transition)
        utils.add_arc_from_to(target_place, new_transition, petri_net)
        utils.add_arc_from_to(new_transition, new_place, petri_net)

   
    if next_transition:
        utils.add_arc_from_to(new_place, next_transition, petri_net)
    else:
        print("No transition found to reconnect the flow.")
    
    print(f"{num_activities} activities added to the Petri net.")
    return petri_net

########################################################################################### EXECUTION
#log_intervals = [10, 16, 26, 43, 71, 117, 193, 316, 517, 848, 1389, 2275, 3727, 6105, 10000]
log_intervals = [2, 8, 18, 35, 63, 109, 185, 308, 509, 840, 1381, 2267, 3719, 6097, 9992]

def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/test/PLG/test_xor/models/xor_pm4py.pnml"
    target_place_id = "14" 
    
    petri_net, initial_marking, final_marking = pnml_importer.apply(pnml_file_path)

    for num_activities in log_intervals:
        
        updated_petri_net = add_activities(petri_net, num_activities, target_place_id)
        
 
        output_file_path = f"/home/l2brb/main/DECpietro/utils/transition_only/finegrade/xor_pm4py_augmented_{num_activities + 8}.pnml"
        
        if updated_petri_net:
            pnml_exporter.apply(updated_petri_net, initial_marking, output_file_path, final_marking=final_marking)
            print(f"Updated Petri net with {num_activities + 8} activities exported to {output_file_path}")

if __name__ == "__main__":
    main()