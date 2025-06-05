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
        
    # # dict id -> name
    # transition_by_id = {
    #     t.get("id"): t.get("name")
    #     for t in workflow_net["transitions"]
    # }
    
    # set to collect names
    atmost1_constraints = set()
    
    for place in workflow_net["places"]:
        if place["id"] not in arc_targets:
            for arc in arcs_by_source.get(place["id"], []):
                trans_id = arc.get("target")
                atmost1_constraints.add(trans_id)
                    
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
        
    # # dict id -> name
    # transition_by_id = {
    #     t.get("id"): t.get("name")
    #     for t in workflow_net.get("transitions", [])
    # }
    
    # set to collect names
    end_constraints = set()
    
    for place in workflow_net.get("places", []):
        if place["id"] not in arc_sources:
            for arc in arcs_by_target.get(place["id"], []):
                trans_id = arc.get("source")
                end_constraints.add(trans_id)
                    
    return [{
        "template": "End",
        "parameters": [list(end_constraints)],
    }]


# RELATION CONSTRAINTS

# Alternate Precedence [if B prev A and not B in between]
def get_alternate_precedence(workflow_net):
    """Return AltPrec constraints using **transition IDs** (no labels)."""

    transition_ids = {t["id"] for t in workflow_net["transitions"]} 
    place_ids = {p["id"] for p in workflow_net["places"]}

    arcs_from_place, arcs_to_place = {}, {}
    for arc in workflow_net["arcs"]:
        src, tgt = arc["source"], arc["target"]
        if src in place_ids:
            arcs_from_place.setdefault(src, set()).add(tgt)   
        if tgt in place_ids:
            arcs_to_place.setdefault(tgt, set()).add(src)     # 

    altprec_constraints = []

    for place in workflow_net["places"]:
        # salta place iniziale o finale
        if place.get("initialMarking") == "1" or place.get("finalMarking") == "1":
            continue

        preds = arcs_to_place.get(place["id"], set()) & transition_ids
        succs = arcs_from_place.get(place["id"], set()) & transition_ids

        if preds and succs:
            altprec_constraints.append({
                "template": "AlternatePrecedence",
                "parameters": [list(preds), list(succs)]
            })

    return altprec_constraints



########################################################### MAIN ##########################################################

# MAIN translate_to_DEC

def translate_to_DEC(workflow_net, model_name):

    
    tasks = [transition["id"] for transition in workflow_net["transitions"]]

    end_constraint = get_end_constraint(workflow_net)
    alternate_precedence = get_alternate_precedence(workflow_net)
    atmost1 = get_atmost1_constraint(workflow_net)

    constraints = []
    constraints.extend(end_constraint)
    constraints.extend(atmost1)
    constraints.extend(alternate_precedence)

    output = {
        "name": model_name,
        "transitions": tasks,
        "constraints": constraints,
    }

    return output
