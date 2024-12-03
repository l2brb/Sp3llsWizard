import random
import string
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils as utils
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

# RULE T2a
# Task t1 is replaced by two conditional tasks t2 and t3. 
# This transformation rule corresponds to the specialization of a task (e.g. handle order) into two more specialized tasks (e.g. handle small order and handle large order).

# Random activity name generator
def generate_random_activity_name():
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{random_suffix}"

# T2a
def replace_random_transition_t2a(petri_net):
    target_transition = random.choice(list(petri_net.transitions)) #TODO   SELEZIONE CASUALE DELLA TRANSITION SU CUI APPLICARE LA TRASFORMAZIONE
    
    
    incoming_places = [arc.source for arc in target_transition.in_arcs]
    outgoing_places = [arc.target for arc in target_transition.out_arcs]
    
    for arc in list(target_transition.in_arcs) + list(target_transition.out_arcs):
        utils.remove_arc(petri_net, arc)
    petri_net.transitions.remove(target_transition)
    
    # t2 e t3
    t2_name = generate_random_activity_name() 
    t3_name = generate_random_activity_name()
    t2 = PetriNet.Transition(t2_name, label=t2_name)
    t3 = PetriNet.Transition(t3_name, label=t3_name)
    petri_net.transitions.add(t2)
    petri_net.transitions.add(t3)
    
    for place in incoming_places:
        utils.add_arc_from_to(place, t2, petri_net)
        utils.add_arc_from_to(place, t3, petri_net)
    
    for place in outgoing_places:
        utils.add_arc_from_to(t2, place, petri_net)
        utils.add_arc_from_to(t3, place, petri_net)
    
    print(f"Transition {target_transition.name} replaced by {t2_name} and {t3_name}.")
    return petri_net

########################################################################################### EXECUTION

intervals = [1, 2, 3, 4, 5, 6, 7]  #TODO: SCALA DA RIVEDERE, DEVO DECIDERE COME APPLICARE LA REGOLA


def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/evaluation/d_contraints/rule/simple-wn.pnml"
    
    petri_net, initial_marking, final_marking = pnml_importer.apply(pnml_file_path)

    for num_activities in intervals:
        updated_petri_net = replace_random_transition_t2a(petri_net)

        output_file_path = f"/home/l2brb/main/DECpietro/evaluation/d_contraints/expanded_pnml/{num_activities}.pnml"
        if updated_petri_net:
            pnml_exporter.apply(updated_petri_net, initial_marking, output_file_path, final_marking=final_marking)
            print(f"Updated WN with {num_activities + 1} activities exported to {output_file_path}")

if __name__ == "__main__":
    main()


