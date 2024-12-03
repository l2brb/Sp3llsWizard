import random
import string
import rule_T1a
import rule_T2a
import rule_T3a
import rule_T4a
import rule_T5a
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter



def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/utils/simple-wn.pnml"
    target_transition_id = "t1"

    petri_net, initial_marking, final_marking = pnml_importer.apply(pnml_file_path)


    for num_places in target_transition_id:
        updated_petri_net = add_places(petri_net, num_places, target_transition_id)
        output_file_path = f"/home/l2brb/main/DECpietro/utils/Trules/Trules_test/trules_aug_{num_places}.pnml"

        if updated_petri_net:
            pnml_exporter.apply(updated_petri_net, initial_marking, output_file_path, final_marking=final_marking)
            print(f"Updated WN with {num_places} places exported to {output_file_path}") 

if __name__ == "__main__":
    main()