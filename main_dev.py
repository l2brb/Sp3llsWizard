import os
import json
import csv

from src.utils import petri_parser
from src.declare_translator import dec_translator_silentremover as dec_translator

def write_to_json(output, output_path: str):
    with open(output_path, 'w') as file:
        json.dump(output, file, indent=4)


def main():
    pnml_file_path = r"C:\Users\lucab\Documents\main\Sp3llsWizard\evaluation\bisimulation\wn\complete_pm4py.pnml"

    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)

    model_name = os.path.basename(pnml_file_path)

    # 2 dec_translator
    if workflow_net:
        output = dec_translator.translate_to_DEC(workflow_net, model_name)
        #print(output)

        #write_to_json(output, r"C:\Users\lucab\Documents\main\Sp3llsWizard\evaluation\bisimulation\wn\complete_dev_pm4py.json")

    
if __name__ == "__main__":
    main()