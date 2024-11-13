import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

# Random activity name generator
def generate_random_activity_name():
    random_suffix = ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
    return f"Activity_{random_suffix}"

# Aggiungo le transition alla petri net copiando quelle esistenti e cambiando il nome delle activity
def add_activities(petri_net, num_activities):
    existing_transitions = list(petri_net.transitions)
    num_existing_transitions = len(existing_transitions)
    
    for _ in range(num_activities):
        # Sceglo a caso una transizione esistente 
        transition_to_copy = random.choice(existing_transitions)
        new_activity_name = generate_random_activity_name()
        new_transition = PetriNet.Transition(new_activity_name, label=new_activity_name)
        petri_net.transitions.add(new_transition)
        
        # Copio gli archi di input e output dalla transition esistente
        for arc in transition_to_copy.in_arcs:
            utils.add_arc_from_to(arc.source, new_transition, petri_net)
        for arc in transition_to_copy.out_arcs:
            utils.add_arc_from_to(new_transition, arc.target, petri_net)

    print(f"{num_activities} activities added to the Petri net.")
    return petri_net

########################################################################################### EXECUTION
log_intervals = [0, 8, 18, 35, 63, 109, 185, 308, 509, 840, 1381, 2267, 3719, 6097, 9992]

def main():
    pnml_file_path = "/Users/l2brb/Documents/main/DECpietro/test/PLG/test_xor/models/xor_pm4py.pnml"
    
    petri_net, initial_marking, final_marking = pnml_importer.apply(pnml_file_path)

    for num_activities in log_intervals:
        
        updated_petri_net = add_activities(petri_net, num_activities)
        
 
        output_file_path = f"{num_activities + 8}.pnml"
        
        if updated_petri_net:
            pnml_exporter.apply(updated_petri_net, initial_marking, output_file_path, final_marking=final_marking)
            print(f"Updated Petri net with {num_activities + 8} activities exported to {output_file_path}")

if __name__ == "__main__":
    main()