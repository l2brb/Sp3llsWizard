from src import petri_parser
from src import dec_translator_target_ultimate as dec_translator
# from src import csv_exporter
from src import json_exporter
from src import wn_json

def main():
    pnml_file_path = "/home/l2brb/main/DECpietro/test/PLG/test_xor/xor_pm4py.pnml"
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)

    if workflow_net:
        print("WORKFLOW NET PARSED SUCCESFULLY.")
        # print(workflow_net)

        # Export WN to JSON
        #wn_json.write_to_json(workflow_net)
        #print("WN JSON EXPORTED.")

      
        # Generate Declarative Constraints
        output = dec_translator.translate_to_DEC(workflow_net)
        print("DECLARATIVE CONTRAINTS GENERATED SUCCESFULLY.")
        #print(output)

        # # Export to CSV
        # csv_exporter.write_to_csv(output)
        # print("CSV EXPORTED SUCCESFULLY.")

        # Export to JSON
        json_exporter.write_to_json(output)
        print("JSON EXPORTED.")



if __name__ == "__main__":
    main()
