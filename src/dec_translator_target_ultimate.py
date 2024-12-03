# import petri_parser
#from memory_profiler import profile


# VERSIONE CON RAGGRUPPAMENTO SOLO SUL TARGET DEL CONSTRAINT

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

"""# Init
#@profile
def get_init_constraint(workflow_net):
    init_constraint = ""
    initial_place_id = None
    for place in workflow_net["places"]:
        if "initialMarking" in place and place["initialMarking"] == "1":
            initial_place_id = place["id"]
            #print(initial_place_id)
            break

    init_constraints = []        
    if initial_place_id:
        for arc in workflow_net["arcs"]:
            if arc["source"] == initial_place_id:
                next_transition_id = arc["target"]
                #print(next_transition_id)
                next_transition_name = [t["name"] for t in workflow_net["transitions"] if t["id"] == next_transition_id][0]
                #print(next_transition_name)
                init_constraints.append(f"{next_transition_name}")
                #print(type(init_constraint))

    result_init = [{
        "template": "Init",
        "parameters": [list(init_constraints)],
    }]

    return result_init"""

# AtMost1
#@profile
def get_atmost1_constraint(workflow_net):
    atmost1_constraint = ""
    initial_place_id = None
    for place in workflow_net["places"]:
        if "initialMarking" in place and place["initialMarking"] == "1":
            initial_place_id = place["id"]
            #print(initial_place_id)
            break

    atmost1_constraints = []        
    if initial_place_id:
        for arc in workflow_net["arcs"]:
            if arc["source"] == initial_place_id:
                next_transition_id = arc["target"]
                #print(next_transition_id)
                next_transition_name = [t["name"] for t in workflow_net["transitions"] if t["id"] == next_transition_id][0]
                #print(next_transition_name)
                atmost1_constraints.append(f"{next_transition_name}")
                #print(type(init_constraint))

    result_atmost1 = [{
        "template": "Atmost1",
        "parameters": [list(atmost1_constraints)],
    }]

    return result_atmost1


# End
##@profile
def get_end_constraint(workflow_net):
    end_constraint = ""
    final_place_id = None
    for place in workflow_net["places"]:
        if "finalMarking" in place and place["finalMarking"] == "1":
            final_place_id = place["id"]
            #print(final_place_id)
            break

    end_constraints = []
    if final_place_id:
        for arc in workflow_net["arcs"]:
            if arc["target"] == final_place_id:
                prev_transition_id = arc["source"]
                #print(prev_transition_id)
                prev_transition_name = [t["name"] for t in workflow_net["transitions"] if t["id"] == prev_transition_id][0]
                end_constraints.append(f"{prev_transition_name}")
    #print(end_constraint)

    result_end = [{
        "template": "End",
        "parameters": [list(end_constraints)],
    }]

    return result_end

# end_constraints = get_end_constraint(workflow_net)
# print(end_constraints)




# RELATION CONSTRAINTS



# Alternate Precedence [if B prev A and not B in between]
#@profile
def get_alternate_precedence(workflow_net):
    constraints = {}

    transition_names = {}
    for transition in workflow_net["transitions"]:
        if transition["id"] == transition["name"]:
            transition_names[transition["id"]] = "t" + transition["name"]
        else:
            transition_names[transition["id"]] = transition["name"]

    for place in workflow_net["places"]:
        if place.get("initialMarking") != "1" and place.get("finalMarking") != "1":
            b = set(arc["target"] for arc in workflow_net["arcs"] if arc["target"] == place["id"])
            #print(b)
            for target in b:
                for arc in workflow_net["arcs"]:
                    if arc["target"] == target:
                        source_transition = transition_names.get(arc["source"])
                        if source_transition:
                            if target not in constraints:
                                constraints[target] = []    #TODO: METTI QUALCHE SET
                            constraints[target].append(source_transition)
    # print("###########################")
    # print(constraints)

    altprecedence_constraint = {}
    for key in constraints.keys():
        for arc in workflow_net["arcs"]:
            if arc["source"] == key:
                # print(arc)
                source_transition = transition_names.get(arc["target"])
                #print(source_transition)
                if source_transition:
                    altprecedence_constraint[source_transition] = constraints[key]

    # print("###########################")
    # print(altprecedence_constraint)
    result_altprec_list = []
    for key, values in altprecedence_constraint.items():
        result_altresp = {
            "template": "AlternatePrecedence",
            "parameters": [list(values), [key]],
        }
        result_altprec_list.append(result_altresp)

    return result_altprec_list



# alt_resp_constraints = get_alternate_precedence(workflow_net)
# print("###########################")
# print(alt_resp_constraints)


# MAIN

def translate_to_DEC(workflow_net):

    model_name = "input_model.pnml" # DEVO AGGIUNGERE IL NOME DEL FILE DAL PATH

    tasks = [transition["name"] for transition in workflow_net["transitions"]]

    #init_constraint = get_init_constraint(workflow_net)
    end_constraint = get_end_constraint(workflow_net)
    alternate_precedence = get_alternate_precedence(workflow_net)
    atmost1 = get_atmost1_constraint(workflow_net)

    constraints = []
    #constraints.extend(init_constraint)
    constraints.extend(end_constraint)
    constraints.extend(atmost1)
    constraints.extend(alternate_precedence)



    output = {
        "name": model_name,
        "tasks": tasks,
        "constraints": constraints,
    }

    return output

# out = translate_to_DEC(workflow_net)
# print(out)