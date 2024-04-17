from src import petri_parser
from src import dec_translator



if __name__ == "__main__":
    pnml_file_path = "/Users/luca/Documents/^main/DECpietro/test/petri_pharma.pnml" 
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
    if workflow_net:
        print("############################# Workflow Net parsed successfully:")
        print(workflow_net)

        constraints = dec_translator.translate_to_DECLARE(workflow_net)
        print("############################# DECLARE Constraints Generated succesfully:")
        for constraint in constraints:
            print(constraint)
        