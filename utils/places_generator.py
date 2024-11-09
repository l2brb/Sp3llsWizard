import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

# Random place name generator
def generate_random_place_name():
    random_suffix = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
    return f"Place_{random_suffix}"


def add_places(petri_net, num_places, target_transition_id):
    target_transition = next((transition for transition in petri_net.transitions if transition.name == target_transition_id), None)
    
    if not target_transition:
        print(f"Transition with id {target_transition_id} not found.")
        return
    next_transition = None
    for arc in target_transition.out_arcs:
        if isinstance(arc.target, PetriNet.Place):
            next_transition = next((arc2.target for arc2 in arc.target.out_arcs if isinstance(arc2.target, PetriNet.Transition)), None)
            if next_transition:
                break
    
    if not next_transition:
        print("No next transition found to reconnect the flow.")
        return
    

    arc_to_remove = next((arc for arc in target_transition.out_arcs if arc.target == next_transition), None)
    if arc_to_remove:
        utils.remove_arc(petri_net, arc_to_remove)
    

    for _ in range(num_places):
        place_name = generate_random_place_name()
        new_place = PetriNet.Place(place_name)
        petri_net.places.add(new_place)
        utils.add_arc_from_to(target_transition, new_place, petri_net)
        utils.add_arc_from_to(new_place, next_transition, petri_net)
    
    print(f"{num_places} places added to the Petri net.")
    return petri_net

########################################################################################### EXECUTION
#log_intervals = [10, 16, 26, 43, 71, 117, 193, 316, 517, 848, 1389, 2275, 3727, 6105, 10000]
log_intervals = [3, 9, 19, 36, 64, 110, 186, 309, 510, 841, 1382, 2268, 3720, 6098, 9993]

def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/test/PLG/test_xor/models/xor_pm4py.pnml"
    target_transition_id = "3"  
    

    petri_net, initial_marking, final_marking = pnml_importer.apply(pnml_file_path)


    for num_places in log_intervals:
        updated_petri_net = add_places(petri_net, num_places, target_transition_id)
        output_file_path = f"/home/l2brb/main/DECpietro/utils/places_only/finegrade/xor_pm4py_augmented_{num_places + 7}.pnml"

        if updated_petri_net:
            pnml_exporter.apply(updated_petri_net, initial_marking, output_file_path, final_marking=final_marking)
            print(f"Updated Petri net with {num_places + 7} places exported to {output_file_path}") 

if __name__ == "__main__":
    main()