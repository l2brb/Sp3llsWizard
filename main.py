import os
import json
import csv
from src import dec_translator_target_source as dec_translator
from utils import petri_parser
# from src import csv_exporter
# from src import wn_json
#from memory_profiler import profile



def write_to_json(output):
    with open('/home/l2brb/main/DECpietro/complete_paper.json', 'w') as file:
        json.dump(output, file)


# def write_to_csv(constraints):
#     with open('/home/l2brb/main/DECpietro/evaluation/bisimulation/reachability_graph/REVISED EASIER_targetsource.csv', 'w', newline='') as file:
#         writer = csv.writer(file)
#         for key, value in constraints.items():
#             writer.writerow([key, value])       


def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/complete_pm4py_paper.pnml"
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)

    if workflow_net:
        print("WORKFLOW NET PARSED SUCCESFULLY.")
        model_name = os.path.basename(pnml_file_path)
        #print(workflow_net["arcs"])
        #print(workflow_net["transitions"])
        #print(workflow_net["places"])
        

        # Export WN to JSON
        #wn_json.write_to_json(workflow_net)
        #print("WN JSON EXPORTED.")

      
        #TESTING BYPASS

        # Generate Declarative Constraints
        output = dec_translator.translate_to_DEC(workflow_net, model_name)
        print("DECLARATIVE CONTRAINTS GENERATED SUCCESFULLY.")
        print(output)

        # # # Export to CSV
        # write_to_csv(output)
        # print("CSV EXPORTED SUCCESFULLY.")
    
        # Export to JSON
        write_to_json(output)
        print("JSON EXPORTED.")

if __name__ == "__main__":  
    main()
