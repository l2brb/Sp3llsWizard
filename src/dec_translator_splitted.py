import csv
"""
translate_to_DECLARE
---------------------------
Translate the Workflow Net to DECLARE constraints.

Args:
- workflow_net: Dictionary representing the Workflow Net.

Returns:
- constraints: List of DECLARE constraints.
"""

# EXISTANCE CONTRAINTS 

# Init
def get_init_constraint(workflow_net):
    init_constraint = ""
    initial_place_id = None
    for place in workflow_net["places"]:
        if "initialMarking" in place and place["initialMarking"] == "1":
            initial_place_id = place["id"]
            #print(initial_place_id)
            break

    if initial_place_id:
        for arc in workflow_net["arcs"]:
            if arc["source"] == initial_place_id:
                next_transition_id = arc["target"]
                #print(next_transition_id)
                next_transition_name = [t["name"] for t in workflow_net["transitions"] if t["id"] == next_transition_id][0]
                #print(next_transition_name)
                init_constraint += f"{next_transition_name}"

    return init_constraint


# End
def get_end_constraint(workflow_net):
    end_constraint = ""
    final_place_id = None
    for place in workflow_net["places"]:
        if "finalMarking" in place and place["finalMarking"] == "1":
            final_place_id = place["idref"]
            print(final_place_id)
            break

    if final_place_id:
        for arc in workflow_net["arcs"]:
            if arc["target"] == final_place_id:
                prev_transition_id = arc["source"]
                prev_transition_name = [t["name"] for t in workflow_net["transitions"] if t["id"] == prev_transition_id][0]
                end_constraint += f"{prev_transition_name})"

    return end_constraint


# RELATION CONSTRAINTS

# Alternate Precedence
def get_alternate_precedence(workflow_net):
    constraints = []
    for transition in workflow_net["transitions"]:
        input_places = [arc["source"] for arc in workflow_net["arcs"] if arc["target"] == transition["id"]]
        output_places = [arc["target"] for arc in workflow_net["arcs"] if arc["source"] == transition["id"]]
        
        for place in input_places:
            for next_place in output_places:
                if next_place != place:
                    constraints.append(f"AlternatePrecedence({place}, {next_place})")
    return constraints


# Alternate Response
def get_alternate_response(workflow_net):
    constraints = []
    for transition in workflow_net["transitions"]:
        input_places = [arc["source"] for arc in workflow_net["arcs"] if arc["target"] == transition["id"]]
        output_places = [arc["target"] for arc in workflow_net["arcs"] if arc["source"] == transition["id"]]
        
        for place in input_places:
            for next_place in output_places:
                if next_place != place:
                    constraints.append(f"AlternateResponse({place}, {next_place})")
    return constraints


# Main Function
def translate_to_DECLARE(workflow_net):
    constraints = []
    constraints.extend(get_init_constraint(workflow_net))
    constraints.extend(get_end_constraint(workflow_net))
    #constraints.extend(get_alternate_precedence(workflow_net))
    #constraints.extend(get_alternate_response(workflow_net))
 
    return constraints





# TESTING FUNCTIONALITY

import petri_parser
if __name__ == "__main__":
    pnml_file_path = "/Users/luca/Documents/^main/DECpietro/petri_test/petri_pharma.pnml" 
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
    if workflow_net:
        print("############################# Workflow Net parsed successfully:")
        print(workflow_net)

        
    
    constraints = get_end_constraint(workflow_net)
    print("DECLARE Constraints:")
    print(constraints)

        


def write_to_csv(constraint_name, activity_name):
    with open('constraints.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Constraint", "Activity"])
        writer.writerow([constraint_name, activity_name])

# Uso della funzione
constraint = "Init"
activity = get_init_constraint(workflow_net)
write_to_csv(constraint, activity)