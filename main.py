from src import petri_parser
from src import dec_translator_update
from src import csv_exporter
from src import json_exporter

def main():
    pnml_file_path = "/home/l2brb/Docker/DECpietro/test/PLG/pm4py/pnml_test_plg.pnml"
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)

    if workflow_net:
        print("WORKFLOW NET PARSED SUCCESFULLY.")
        # print(workflow_net)
      
        # Generate Declarative Constraints
        output = dec_translator_update.translate_to_DEC(workflow_net)
        print("DECLARATIVE CONTRAINTS GENERATED SUCCESFULLY.")
        #print(constraints)

        # # Export to CSV
        # csv_exporter.write_to_csv(output)
        # print("CSV EXPORTED SUCCESFULLY.")

        # Export to JSON
        json_exporter.write_to_json(output)
        print("JSON EXPORTED.")

if __name__ == "__main__":
    main()
