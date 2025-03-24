# TARGET SOURCE VERSION W/SILENT BYPASS

"""
translate_to_DECLARE
---------------------------
Translate the Workflow Net into a subset of DECLARE constraints.

Args:
- workflow_net: Dictionary representing the Workflow Net.

Returns:
- constraints: List of DECLARE constraints w/silent transitions reduction.
"""


################################################# EXISTANCE CONTRAINTS

# AtMost1
#@profile

#TODO: QUI LA LOGICA DI SISNTESI DELLE SILENT CON START ARTIFICIALE

def get_atmost1_constraint(workflow_net):
    atmost1_constraints = []     
    
    for place in workflow_net["places"]:
        if not any(arc.get("target") == place["id"] for arc in workflow_net["arcs"]):
            for arc in workflow_net["arcs"]:
                if arc.get("source") == place["id"]:
                    transition_id = arc.get("target")

                    transition = next(
                        (t for t in workflow_net["transitions"] if t.get("id") == transition_id),
                        None
                    )
                    if transition:
                        transition_name = transition.get("name")
                        if transition_name not in atmost1_constraints:
                            atmost1_constraints.append(transition_name)
   
    result_atmost1 = [{
        "template": "Atmost1",
        "parameters": [list(atmost1_constraints)],
    }]

    return result_atmost1



#TODO: QUI LA LOGICA DI SISNTESI DELLE SILENT CON START ARTIFICIALE

# End
#@profile
def get_end_constraint(workflow_net):
    end_constraints = []

    for place in workflow_net.get("places", []):

        if not any(arc.get("source") == place["id"] for arc in workflow_net.get("arcs", [])):
            for arc in workflow_net.get("arcs", []):    
                if arc.get("target") == place["id"]:
                    transition_id = arc.get("source")

                    transition = next(
                        (t for t in workflow_net.get("transitions", []) if t.get("id") == transition_id),
                        None
                    )
                    if transition:
                        transition_name = transition.get("name")
                        if transition_name not in end_constraints:
                            end_constraints.append(transition_name)

    result_end = [{
        "template": "End",
        "parameters": [list(end_constraints)],
    }]

    return result_end


################################################# RELATION CONSTRAINTS

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
    mapping = {}


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


        key = tuple(pred_transitions) if len(pred_transitions) > 1 else next(iter(pred_transitions), None)
        if key is not None:
            mapping.setdefault(key, []).append(list(succ_transitions))

    #print(mapping)
    return altprecedence_constraints



################################################# MAIN

def translate_to_DEC(workflow_net, model_name):

    
    tasks = [transition["name"] for transition in workflow_net["transitions"] if not transition["is_tau"]]

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






#TODO: EXTRA ALTRESP IMPLEMENTATION

""" 

# Alternate Response [if A than B and not A in between]

def get_alternate_response(workflow_net):
    # Costruisco il mapping
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

    altresp_constraints = []

    for place in workflow_net["places"]:
        if place.get("initialMarking") == "1" or place.get("finalMarking") == "1":
            continue  

        place_id = place["id"]

        predecessors = arcs_to_place.get(place_id, set())
        successors = arcs_from_place.get(place_id, set())
   

        # TODO: Bug here 
        print(f"Place ID: {place_id}")
        print(f"Raw Predecessors: {predecessors}")
        print(f"Raw Successors: {successors}")


        # Converte gli ID delle transizioni in nomi
        pred_transitions = {transition_names[t_id] for t_id in predecessors if t_id in transition_names}
        succ_transitions = {transition_names[t_id] for t_id in successors if t_id in transition_names}

        for succ in succ_transitions:
            if pred_transitions:
                altresp_constraints.append({
                    "template": "AlternatePrecedence",
                    "parameters": [list(pred_transitions), [succ]],
                })

    return altresp_constraints


"""



"""# TAU IDENTIFIER

def get_visible_tasks(workflow_net):
    return [transition["name"] for transition in workflow_net["transitions"] if transition["is_tau"]]"""



"""def get_alternate_precedence(workflow_net):
    # Costruisco il mapping
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

        # predecessors = arcs_to_place.get(place_id, set())
        # successors = arcs_from_place.get(place_id, set())
   
        # BYPASS DELLE SILENT durante la lettura degli altprec
        
        raw_predecessors = arcs_to_place.get(place_id, set())
        raw_successors = arcs_from_place.get(place_id, set())

        # Bypass silent transitions per trovare prec e succ visibili
        pred_transitions = set()
        for pred in raw_predecessors:
            pred_transitions.update(bypass_silent_transitions(workflow_net, pred, direction="backward"))

        succ_transitions = set()
        for succ in raw_successors:
            succ_transitions.update(bypass_silent_transitions(workflow_net, succ, direction="forward"))


        # TODO: Bug qui
        print(f"Place ID: {place_id}")
        print(f"Raw Predecessors: {raw_predecessors}, Visible Predecessors: {pred_transitions}")
        print(f"Raw Successors: {raw_successors}, Visible Successors: {succ_transitions}")


        # Converte gli ID delle transizioni in nomi
        pred_transitions = {transition_names[t_id] for t_id in pred_transitions if t_id in transition_names}
        succ_transitions = {transition_names[t_id] for t_id in succ_transitions if t_id in transition_names}


        for succ in succ_transitions:
            if pred_transitions and succ_transitions:
                altprecedence_constraints.append({
                    "template": "AlternatePrecedence",
                    "parameters": [list(pred_transitions), list(succ_transitions)],
                })

    return altprecedence_constraints"""


