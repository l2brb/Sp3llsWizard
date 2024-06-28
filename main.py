from src import petri_parser
from src import dec_translator
from src import csv_exporter
from src import json_exporter


if __name__ == "__main__":
    pnml_file_path = "/Users/luca/Documents/^main/DECpietro/test/hospital.pnml" 
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)

    if workflow_net:
        print("######################### Workflow Net parsed successfully! #######################")
        #print(workflow_net["transitions"])

        constraints = dec_translator.translate_to_DEC(workflow_net)
        print("################# Declarative Constraints Generated succesfully! ##################")
        # print(constraints)

        csv_exporter.write_to_csv(constraints)
        print("############################# CSV Exported Correctly! #############################") 


        json_exporter.write_to_json(constraints)
        print("############################# json Exported Correctly! #############################")