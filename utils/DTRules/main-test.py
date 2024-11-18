import random
import string
import rule_T1a
import rule_T3a
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter



def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/utils/simple-wn.pnml"
    petri_net, initial_marking, final_marking = pnml_importer.apply(pnml_file_path)

    # Number of times to apply the transformation
    num_applications = 2

    # T1a - CONSECUTIVE TASKS
    for i in range(num_applications):
        target_transition = "t1"
        t2_name = "t1" if i == 1 else "prova"
        t3_name = "t1" if i != 1 else "prova_2"
        updated_petri_net = rule_T1a.extend_transition_t1a(petri_net, target_transition, t2_name, t3_name)

     #T3a - AND SPLIT
    target_transition = "t1"
    t2_name = "t1"
    t3_name = "provaprova"
    updated_petri_net = rule_T3a.and_split_transition_t3a(petri_net, target_transition, t2_name, t3_name)   


    output_file_path = f"/home/l2brb/main/DECpietro/utils/DTRules/out/T3a_augmented_test.pnml"
    if updated_petri_net:
        pnml_exporter.apply(updated_petri_net, initial_marking, output_file_path, final_marking=final_marking)
        print(f"Updated WN")

if __name__ == "__main__":
    main()