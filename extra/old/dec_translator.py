
"""
translate_to_DECLARE
---------------------------
Translate the Workflow Net to DECLARE constraints.

Args:
- workflow_net: Dictionary representing the Workflow Net.

Returns:
- constraints: List of DECLARE constraints.
"""

def translate_to_DECLARE(workflow_net):

    constraints = []

    # Init and End Constraints
    init_constraint = "Init("
    end_constraint = "End("
    
    for place in workflow_net["places"]:
        if "initialMarking" in place and place["initialMarking"] == "true":
            init_constraint += f"{place['id']}, "
        if "finalMarking" in place and place["finalMarking"] == "true":
            end_constraint += f"{place['id']}, "
    
    init_constraint = init_constraint.rstrip(", ") + ")"
    end_constraint = end_constraint.rstrip(", ") + ")"
    
    constraints.extend([init_constraint, end_constraint])

    # Alternate Precedence and Alternate Response constraints
    for transition in workflow_net["transitions"]:
        input_places = [arc["source"] for arc in workflow_net["arcs"] if arc["target"] == transition["id"]]
        output_places = [arc["target"] for arc in workflow_net["arcs"] if arc["source"] == transition["id"]]
        
        for place in input_places:
            for next_place in output_places:
                if next_place != place:
                    constraints.append(f"AlternatePrecedence({place}, {next_place})")
                    constraints.append(f"AlternateResponse({place}, {next_place})")

    return constraints




"""# TESTING FUNCTIONALITY
import petri_parser
if __name__ == "__main__":
    pnml_file_path = "/Users/luca/Documents/^main/DECpietro/petri_test/petri_pharma.pnml" 
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
    if workflow_net:
        print("############################# Workflow Net parsed successfully:")
        print(workflow_net)

        
    
    constraints = translate_to_DECLARE(workflow_net)
    print("DECLARE Constraints:")
    for constraint in constraints:
        print(constraint)"""
