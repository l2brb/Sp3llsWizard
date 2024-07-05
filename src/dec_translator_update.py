"""
translate_to_DECLARE
---------------------------
Translate the Workflow Net to Declarative constraints.

Args:
- workflow_net: Dictionary representing the Workflow Net.

Returns:
- constraints: List of Declarative constraints.
"""

# pnml_file_path = "/home/l2brb/Docker/DECpietro/test/PLG/pm4py/pnml_test_plg.pnml"
# workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
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

    result_init = [{
        "template": "Init",
        "parameters": [[init_constraint]],
        "support": 1.0,
        "confidence": 1.0,
        "interestFactor": 1.0
    }]

    return result_init


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

    result_end = [{
        "template": "End",
        "parameters": [[end_constraint]],
        "support": 1.0,
        "confidence": 1.0,
        "interestFactor": 1.0
    }]

    return result_end

# end_constraints = get_end_constraint(workflow_net)
# print(end_constraints)




# RELATION CONSTRAINTS


# Alternate Precedence
def get_alternate_precedence(workflow_net):
    constraints = {}

    transition_names = {}
    for transition in workflow_net["transitions"]:
        if transition["id"] == transition["name"]:
            transition_names[transition["id"]] = "SILENT_" + transition["name"]
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

    result_altprec_list = []
    for key, value in altprecedence_constraint.items():
        result_altresp = {
        "template": "AlternatePrecedence",
        "parameters": [[key], [value]],
        "support": 1.0,
        "confidence": 1.0,
        "interestFactor": 1.0
    }
        result_altprec_list.append(result_altresp)

    return result_altprec_list

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

    result_altresp_list = []
    for key, value in altresponse_constraint.items():
        result_altresp = {
        "template": "AlternateResponse",
        "parameters": [[key], [value]],
        "support": 1.0,
        "confidence": 1.0,
        "interestFactor": 1.0
    }
        result_altresp_list.append(result_altresp)

    return result_altresp_list



# alt_resp_constraints = get_alternate_response(workflow_net)
# print(alt_resp_constraints)




def translate_to_DEC(workflow_net):

    model_name = "input_model.pnml" # DEVO AGGIUNGERE IL NOME DEL FILE DAL PATH

    tasks = [transition["name"] for transition in workflow_net["transitions"]]

    init_constraint = get_init_constraint(workflow_net)
    end_constraint = get_end_constraint(workflow_net)
    alternate_precedence = get_alternate_precedence(workflow_net)
    alternate_response = get_alternate_response(workflow_net)

    constraints = []
    constraints.extend(init_constraint)
    constraints.extend(end_constraint)
    constraints.extend(alternate_precedence)
    constraints.extend(alternate_response)

    output = {
        "name": model_name,
        "tasks": tasks,
        "constraints": constraints
    }

    return output

# out = translate_to_DEC(workflow_net)
# print(out)