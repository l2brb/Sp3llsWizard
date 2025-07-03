import os
import json


from src.utils import petri_parser
from src.declare_translator import dec_translator_silent as dec_translator


PNML_PATH = "/Users/l2brb/Documents/main/DECpietro/conformance/logtesting/testone/testone_pm4py.pnml"
JSON_PATH = "/Users/l2brb/Documents/main/DECpietro/conformance/logtesting/testone/testone_pm4py.json"

def write_to_json(output, output_path: str):
    with open(output_path, 'w') as file:
        json.dump(output, file, indent=4)

def main():
    pnml_file_path = PNML_PATH 

    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
    #print(workflow_net)

    # Get the name from the .pnml file
    model_name = os.path.basename(pnml_file_path)

    if workflow_net:
        output = dec_translator.translate_to_DEC(workflow_net, model_name)
        #print(output)
        write_to_json(output, JSON_PATH) 
        print(json.dumps(output, indent=4))  
    
if __name__ == "__main__":
    main()