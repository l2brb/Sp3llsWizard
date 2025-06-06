import os
import json


from src.utils import petri_parser
from src.declare_translator import dec_translator_nolables as dec_translator

def write_to_json(output, output_path: str):
    with open(output_path, 'w') as file:
        json.dump(output, file, indent=4)


def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/conformance/wnsample/sketch/FIG1.pnml"  

    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
    #print(workflow_net)


    model_name = os.path.basename(pnml_file_path)

    # 2 dec_translator
    if workflow_net:
        output = dec_translator.translate_to_DEC(workflow_net, model_name)
        print(output)

        write_to_json(output, "/home/l2brb/main/DECpietro/conformance/wnsample/sketch/FIG1.json") 
    
if __name__ == "__main__":
    main()