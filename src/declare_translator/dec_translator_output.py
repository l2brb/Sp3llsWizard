# TARGET SOURCE BRANCHING VERSION

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

def get_atmost1_constraint(workflow_net):
    # Arc target set
    arc_targets = {arc.get("target") for arc in workflow_net["arcs"]}
    
    # group by source
    arcs_by_source = {}
    for arc in workflow_net["arcs"]:
        source = arc.get("source")
        arcs_by_source.setdefault(source, []).append(arc)
        
    # dict id -> name
    transition_by_id = {
        t.get("id"): t.get("name")
        for t in workflow_net["transitions"]
    }
    
    # set to collect names
    atmost1_constraints = set()
    
    for place in workflow_net["places"]:
        if place["id"] not in arc_targets:
            for arc in arcs_by_source.get(place["id"], []):
                transition_name = transition_by_id.get(arc.get("target"))
                if transition_name:
                    atmost1_constraints.add(transition_name)
                    
    return [{
        "template": "Atmost1",
        "parameters": [list(atmost1_constraints)],
    }]


# End
def get_end_constraint(workflow_net):
    # Arc source set
    arc_sources = {arc.get("source") for arc in workflow_net.get("arcs", [])}
    
    # group by target
    arcs_by_target = {}
    for arc in workflow_net.get("arcs", []):
        target = arc.get("target")
        arcs_by_target.setdefault(target, []).append(arc)
        
    # dict id -> name
    transition_by_id = {
        t.get("id"): t.get("name")
        for t in workflow_net.get("transitions", [])
    }
    
    # set to collect names
    end_constraints = set()
    
    for place in workflow_net.get("places", []):
        if place["id"] not in arc_sources:
            for arc in arcs_by_target.get(place["id"], []):
                transition_name = transition_by_id.get(arc.get("source"))
                if transition_name:
                    end_constraints.add(transition_name)
                    
    return [{
        "template": "End",
        "parameters": [list(end_constraints)],
    }]


# RELATION CONSTRAINTS

# Alternate Precedence [if B prev A and not B in between]
def get_alternate_precedence(workflow_net):

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

        if pred_transitions and succ_transitions:
            altprecedence_constraints.append({
                "template": "AlternatePrecedence",
                "parameters": [list(pred_transitions), list(succ_transitions)],
            })

    return altprecedence_constraints



########################################################### MAIN ##########################################################

# MAIN translate_to_DEC

def translate_to_DEC(workflow_net, model_name):

    mapping = {}
    for t in workflow_net["transitions"]:
        name = t.get("name")
        id_ = t["id"]
        mapping.setdefault(name, []).append(id_)
    
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
        "tramsitionsMap": mapping,
        "tasks": tasks,
        "constraints": constraints,
    }

    return output
