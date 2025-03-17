# import petri_parser
#from memory_profiler import profile


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

# pnml_file_path = "/home/l2brb/Docker/DECpietro/test/PLG/pm4py/pnml_test_plg.pnml"
# workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
# print(workflow_net)


# activity_a_name = [t["name"] for t in workflow_net["transitions"]]
# print(activity_a_name)


# EXISTANCE CONTRAINTS

# AtMost1
#@profile
def get_atmost1_constraint(workflow_net):
    # Pre-calcola il set dei target degli archi
    arc_targets = {arc.get("target") for arc in workflow_net["arcs"]}
    
    # Raggruppa gli archi per source
    arcs_by_source = {}
    for arc in workflow_net["arcs"]:
        source = arc.get("source")
        arcs_by_source.setdefault(source, []).append(arc)
        
    # Crea un dizionario: id della transizione -> nome della transizione
    transition_by_id = {
        t.get("id"): t.get("name")
        for t in workflow_net["transitions"]
    }
    
    # Usa un set per raccogliere i nomi (evita duplicati)
    atmost1_constraints = set()
    
    for place in workflow_net["places"]:
        # Se il posto non è un target di alcun arco
        if place["id"] not in arc_targets:
            # Itera solo sugli archi che partono da questo posto
            for arc in arcs_by_source.get(place["id"], []):
                transition_name = transition_by_id.get(arc.get("target"))
                if transition_name:
                    atmost1_constraints.add(transition_name)
                    
    return [{
        "template": "Atmost1",
        "parameters": [list(atmost1_constraints)],
    }]


# End
#@profile
def get_end_constraint(workflow_net):
    # Pre-calcola il set delle sorgenti degli archi
    arc_sources = {arc.get("source") for arc in workflow_net.get("arcs", [])}
    
    # Raggruppa gli archi per target
    arcs_by_target = {}
    for arc in workflow_net.get("arcs", []):
        target = arc.get("target")
        arcs_by_target.setdefault(target, []).append(arc)
        
    # Dizionario: id della transizione -> nome della transizione
    transition_by_id = {
        t.get("id"): t.get("name")
        for t in workflow_net.get("transitions", [])
    }
    
    # Usa un set per raccogliere i nomi
    end_constraints = set()
    
    for place in workflow_net.get("places", []):
        # Se il posto non è una sorgente di alcun arco
        if place["id"] not in arc_sources:
            # Itera solo sugli archi che arrivano a questo posto
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
#@profile
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
