#from memory_profiler import profile

# VERSIONE CON RAGGRUPPAMENTO SOLO SUL TARGET

"""
translate_to_DECLARE
---------------------------
Translate the Workflow Net to Declarative constraints.

Args:
- workflow_net: Dictionary representing the Workflow Net.

Returns:
- constraints: List of Declarative constraints.
"""


# EXISTANCE CONTRAINTS

# AtMost1
#@profile
def get_atmost1_constraint(workflow_net):
    atmost1_constraint = ""
    initial_place_id = None
    for place in workflow_net["places"]:
        if "initialMarking" in place and place["initialMarking"] == "1":
            initial_place_id = place["id"]
            break

    atmost1_constraints = []        
    if initial_place_id:
        for arc in workflow_net["arcs"]:
            if arc["source"] == initial_place_id:
                next_transition_id = arc["target"]
                next_transition_name = [t["name"] for t in workflow_net["transitions"] if t["id"] == next_transition_id][0]
                atmost1_constraints.append(f"{next_transition_name}")

    result_atmost1 = [{
        "template": "Atmost1",
        "parameters": [list(atmost1_constraints)],
    }]

    return result_atmost1


# End
#@profile
def get_end_constraint(workflow_net):
    end_constraint = ""
    final_place_id = None
    for place in workflow_net["places"]:
        if "finalMarking" in place and place["finalMarking"] == "1":
            final_place_id = place["id"]
            break

    end_constraints = []
    if final_place_id:
        for arc in workflow_net["arcs"]:
            if arc["target"] == final_place_id:
                prev_transition_id = arc["source"]
                prev_transition_name = [t["name"] for t in workflow_net["transitions"] if t["id"] == prev_transition_id][0]
                end_constraints.append(f"{prev_transition_name}")

    result_end = [{
        "template": "End",
        "parameters": [list(end_constraints)],
    }]

    return result_end


# RELATION CONSTRAINTS

# Alternate Precedence [if B prev A and not B in between]

#@profile
def get_alternate_precedence(workflow_net):
    # Costruisci mapping per accesso rapido
    transition_names = {t["id"]: t["name"] for t in workflow_net["transitions"]}
    places_ids = set(place["id"] for place in workflow_net["places"])

    arcs_from_place = {}
    arcs_to_place = {}

    for arc in workflow_net["arcs"]:
        source = arc["source"]
        target = arc["target"]

        if source in places_ids:
            arcs_from_place.setdefault(source, set()).add(target)
        if target in places_ids:
            arcs_to_place.setdefault(target, set()).add(source)

    altprecedence_constraints = []

    for place in workflow_net["places"]:
        if place.get("initialMarking") == "1" or place.get("finalMarking") == "1":
            continue  

        place_id = place["id"]

        predecessors = arcs_to_place.get(place_id, set())
        successors = arcs_from_place.get(place_id, set())

        pred_transitions = {transition_names[t_id] for t_id in predecessors if t_id in transition_names}
        succ_transitions = {transition_names[t_id] for t_id in successors if t_id in transition_names}

        for succ in succ_transitions:
            if pred_transitions:
                altprecedence_constraints.append({
                    "template": "AlternatePrecedence",
                    "parameters": [list(pred_transitions), [succ]],
                })

    return altprecedence_constraints




# MAIN

def translate_to_DEC(workflow_net, model_name):

    
    tasks = [transition["name"] for transition in workflow_net["transitions"]]

    end_constraint = get_end_constraint(workflow_net)
    alternate_precedence = get_alternate_precedence(workflow_net)
    atmost1 = get_atmost1_constraint(workflow_net)

    constraints = []
    constraints.extend(end_constraint)
    constraints.extend(atmost1)
    constraints.extend(alternate_precedence)

    output = {
        "name": model_name,
        "tasks": tasks,
        "constraints": constraints,
    }

    return output
