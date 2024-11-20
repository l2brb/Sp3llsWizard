import random
import string
import rule_T1a
import rule_T3a
import rule_T2a
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter


def generate_random_place_name():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(5))


def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/utils/simple-wn.pnml"
    petri_net, initial_marking, final_marking = pnml_importer.apply(pnml_file_path)


    # Fisso il p1 e p2 TODO: magari devo trovare una maniera migliore ma funziona
    target_transition = next((t for t in petri_net.transitions if t.name == 't1'), None)
    if target_transition:
        incoming_places = [arc.source for arc in target_transition.in_arcs]
        outgoing_places = [arc.target for arc in target_transition.out_arcs]

        if incoming_places:
            incoming_places[0].name = 'p1'
        if outgoing_places:
            outgoing_places[0].name = 'p2'

    
    num__T2_applications = 2

    for iteration in range(2):
       
        # T1a - CONSECUTIVE TASKS
        for i in range(num__T2_applications):
            target_transition = "t1"
            t2_name = "t1" if i == 1 else None
            t3_name = "t1" if i != 1 else None
            intermediate_place_name = None
            updated_petri_net = rule_T1a.extend_transition_t1a(petri_net, target_transition, t2_name, t3_name, intermediate_place_name)
            
        # T3a - AND SPLIT
        target_transition = "t1"
        t2_name = "t1"
        t3_name = None
        updated_petri_net = rule_T3a.and_split_transition_t3a(petri_net, target_transition, t2_name, t3_name)  
    
        # T2a - XOR SPLIT
        t3_name = None
        updated_petri_net = rule_T2a.xor_split_transition_t2a(petri_net, t3_name)

        # T4a - LOOP
        #updated_petri_net = rule_T4a.loop_transition_t4a(petri_net, t3_name)

        # Rename p1 and p2 to random names
        p1 = next((p for p in petri_net.places if p.name == 'p1'), None)
        p2 = next((p for p in petri_net.places if p.name == 'p2'), None)
        if p1:
            p1.name = generate_random_place_name()
        if p2:
            p2.name = generate_random_place_name()

        
        # Save the output for each iteration
        output_file_path = f"/home/l2brb/main/DECpietro/utils/DTRules/out/T1a_augmented_test_{iteration}.pnml"
        pnml_exporter.apply(updated_petri_net, initial_marking, output_file_path, final_marking=final_marking)
        # print(f"Updated WN saved to {output_file_path}")

        # Use the updated Petri net for the next iteration
        petri_net = updated_petri_net

if __name__ == "__main__":
    main()



#######################################################################################################################

"""
def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/utils/simple-wn.pnml"
    petri_net, initial_marking, final_marking = pnml_importer.apply(pnml_file_path)

    # Number of times to apply the transformation
    num_applications = 2

    # T1a - CONSECUTIVE TASKS
    for i in range(num_applications):
        target_transition = "t1"
        t2_name = "t1" if i == 1 else None
        t3_name = "t1" if i != 1 else None
        intermediate_place_name = None
        updated_petri_net = rule_T1a.extend_transition_t1a(petri_net, target_transition, t2_name, t3_name, intermediate_place_name)

    # # T3a - AND SPLIT
    target_transition = "t1"
    t2_name = "t1"
    t3_name = None
    updated_petri_net = rule_T3a.and_split_transition_t3a(petri_net, target_transition, t2_name, t3_name)  
    
    # # T2a - XOR SPLIT
    # target_transition = "t1"
    # t2_name = "t1"
    # t3_name = "provaprova"
    # updated_petri_net = rule_T3a.and_split_transition_t3a(petri_net, target_transition, t2_name, t3_name) 
    
    # # T4a - LOOP
    # target_transition = "t1"
    # t2_name = "t1"
    # t3_name = "provaprova"
    # updated_petri_net = rule_T3a.and_split_transition_t3a(petri_net, target_transition, t2_name, t3_name) 
    

    output_file_path = f"/home/l2brb/main/DECpietro/utils/DTRules/out/T3a_augmented_test.pnml"
    if updated_petri_net:
        pnml_exporter.apply(updated_petri_net, initial_marking, output_file_path, final_marking=final_marking)
        print(f"Updated WN")

if __name__ == "__main__":
    main()"""
