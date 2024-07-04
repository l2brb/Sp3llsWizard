import petri_parser

"""
translate_to_DECLARE
---------------------------
Translate the Workflow Net to Declarative constraints.

Args:
- workflow_net: Dictionary representing the Workflow Net.

Returns:
- constraints: List of Declarative constraints.
"""

pnml_file_path = "/home/l2brb/Docker/DECpietro/test/PLG/pm4py/pnml_test_plg.pnml"
workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
# print(workflow_net)


# activity_a_name = [t["name"] for t in workflow_net["transitions"]]
# print(activity_a_name)



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
                #print(type(init_constraint))

    return {"Init": init_constraint}


# End
def get_end_constraint(workflow_net):
    end_constraint = ""
    final_place_id = None
    for place in workflow_net["places"]:
        if "finalMarking" in place and place["finalMarking"] == "1":
            final_place_id = place["id"]
            #print(final_place_id)
            break

    if final_place_id:
        for arc in workflow_net["arcs"]:
            if arc["target"] == final_place_id:
                prev_transition_id = arc["source"]
                #print(prev_transition_id)
                prev_transition_name = [t["name"] for t in workflow_net["transitions"] if t["id"] == prev_transition_id][0]
                end_constraint += f"{prev_transition_name}"

    return {"End": end_constraint}


# RELATION CONSTRAINTS


# activity_a_name = [t["name"] for t in workflow_net["transitions"]]
# print(activity_a_name)][0]


# Alternate Precedence
def get_alternate_precedence(workflow_net):
    constraints = {}

    transition_names = {}
    for transition in workflow_net["transitions"]:
        if transition["id"] == transition["name"]:
            transition_names[transition["id"]] = "" + transition["name"]
        else:
            transition_names[transition["id"]] = transition["name"]

    for place in workflow_net["places"]:
        if place.get("initialMarking") != "1" and place.get("finalMarking") != "1":
            a = set(arc["source"] for arc in workflow_net["arcs"] if arc["source"] == place["id"])
            for source in a:
                for arc in workflow_net["arcs"]:
                    if arc["source"] == source:
                        target_transition = transition_names.get(arc["target"])
                        if target_transition:
                            constraints[source] = target_transition

    altprecedence_constraint = {}
    for key in constraints.keys():
        for arc in workflow_net["arcs"]:
            if arc["target"] == key:
                source_transition = transition_names.get(arc["source"])
                if source_transition:
                    altprecedence_constraint[source_transition] = constraints[key]

    return {"AltPrecedence": altprecedence_constraint}

# alt_prec_contraints = get_alternate_precedence(workflow_net)
# print(alt_prec_contraints)



# Alternate Response
def get_alternate_response(workflow_net):
    constraints = {}

    transition_names = {}
    for transition in workflow_net["transitions"]:
        if transition["id"] == transition["name"]:
            transition_names[transition["id"]] = "" + transition["name"]
        else:
            transition_names[transition["id"]] = transition["name"]

    for place in workflow_net["places"]:
        if place.get("initialMarking") != "1" and place.get("finalMarking") != "1":
            b = set(arc["target"] for arc in workflow_net["arcs"] if arc["target"] == place["id"])
            for target in b:
                for arc in workflow_net["arcs"]:
                    for transition in workflow_net["transitions"]:
                        if arc["target"] == target and arc["source"] == transition["id"]:
                            source_name = transition_names.get(arc["source"])
                            if source_name:
                                constraints[source_name] = target

    altresponse_constraint = {}
    for key, val in constraints.items():
        for arc in workflow_net["arcs"]:
            if arc["source"] == val:
                target_name = transition_names.get(arc["target"])
                if target_name:
                    altresponse_constraint[key] = target_name

    return {"AltResponse": altresponse_constraint}


alt_resp_constraints = get_alternate_response(workflow_net)
print(alt_resp_constraints)


# Main Function
def translate_to_DEC(workflow_net):
    constraints = get_init_constraint(workflow_net)
    constraints = constraints | get_end_constraint(workflow_net)
    constraints = constraints | get_alternate_precedence(workflow_net)
    constraints = constraints | get_alternate_response(workflow_net)


    return constraints


