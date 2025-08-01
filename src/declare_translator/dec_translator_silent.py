# TARGET SOURCE BRANCHING VERSION W/SILENT BYPASS

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

def get_atmost1_constraint(workflow_net):
    # Arc target set
    arc_targets = {arc.get("target") for arc in workflow_net["arcs"]}
    #rint(arc_targets)
    
    # group by source
    arcs_by_source = {}
    for arc in workflow_net["arcs"]:
        source = arc.get("source")
        #print(source)
        arcs_by_source.setdefault(source, []).append(arc)
    #print(arcs_by_source)
        
    # dict id -> name
    transition_by_id = {
        t.get("id"): (t.get("name"), t.get("is_tau", False))
        for t in workflow_net["transitions"]
    }
    
    # set to collect names
    atmost1_constraints = set()
    
    for place in workflow_net["places"]:
        if place["id"] not in arc_targets: # @TODO check is_tau here
            for arc in arcs_by_source.get(place["id"], []):
                # NEW HERE
                transition_id = arc.get("target")
                transition_name, is_tau = transition_by_id.get(transition_id, (None, False))
                #print(transition_name, is_tau)
                
                if is_tau:
                    # if tau -> substitute with artificial "START"
                    atmost1_constraints.add("START")
                elif transition_name:
                    atmost1_constraints.add(transition_name)
                #print(atmost1_constraints)
             
                # transition_name = transition_by_id.get(arc.get("target"))
                # if transition_name:
                #     atmost1_constraints.add(transition_name)
                    
                    
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
        t.get("id"): (t.get("name"), t.get("is_tau", False))
        for t in workflow_net["transitions"]
    }
    
    # set to collect names
    end_constraints = set()
    
    for place in workflow_net.get("places", []):
        if place["id"] not in arc_sources: 
            # NEW HERE
            for arc in arcs_by_target.get(place["id"], []):
                transition_id = arc.get("source")
                transition_name, is_tau = transition_by_id.get(transition_id, (None, False))
                #print(transition_name, is_tau)
                
                if is_tau:
                    end_constraints.add("END")
                elif transition_name:
                    end_constraints.add(transition_name)
                #print(end_constraints)

            #     transition_name = transition_by_id.get(arc.get("source"))
            #     if transition_name:
            #         end_constraints.add(transition_name)
                    
    return [{
        "template": "End",
        "parameters": [list(end_constraints)],
    }]


################################################# RELATION CONSTRAINTS

# Alternate Precedence [if B prev A and not B in between]

def get_alternate_precedence(workflow_net):
    # transition names mapping 
    transition_names = {t["id"]: t["name"] for t in workflow_net["transitions"]}
    # set of place IDs
    places_ids = set(place["id"] for place in workflow_net["places"])

    arcs_from_place = {}
    arcs_to_place = {}

    # group arcs by source and target
    for arc in workflow_net["arcs"]:
        source = arc["source"]
        target = arc["target"]

        if source in places_ids:
            arcs_from_place.setdefault(source, set()).add(target) # source -> target
        if target in places_ids:
            arcs_to_place.setdefault(target, set()).add(source) # target -> source

    altprecedence_constraints = [] 

    # Iterate over places to find constraints
    for place in workflow_net["places"]:
        if place.get("initialMarking") == "1" or place.get("finalMarking") == "1":  # un pò una merdina posso far qualcosa di meglio per sta cosa
            continue # skip initial and final places

        place_id = place["id"]

        predecessors = arcs_to_place.get(place_id, set())
        successors = arcs_from_place.get(place_id, set())

        pred_transitions = {transition_names[t_id] for t_id in predecessors if t_id in transition_names}
        succ_transitions = {transition_names[t_id] for t_id in successors if t_id in transition_names}

        # append constraints
        if pred_transitions and succ_transitions:
            altprecedence_constraints.append({
                "template": "AlternatePrecedence",
                "parameters": [pred_transitions, succ_transitions]
                #"parameters": [list(pred_transitions), list(succ_transitions)],
                #"place_id": place_id  # aggiunto place_id per distinzione
            })

    return altprecedence_constraints


################################################# AltPrec Silent Synthesis

# Replacement Finder (transitive closure per silent)

def compute_silent_replacements(workflow_net, silent_labels):
    transition_names = {t["id"]: t["name"] for t in workflow_net["transitions"]}
    print(transition_names)
    print("cazzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
    place_ids = {place["id"] for place in workflow_net["places"]}

    arcs_from_transition = {}
    arcs_from_place = {}
    
    # group arcs by source and target
    for arc in workflow_net["arcs"]:
        src, tgt = arc["source"], arc["target"]
        print(f"rosita",src, tgt)
        if src in transition_names:
            print (f"micaspicci",src)
            print("cazzomannaggia")
            arcs_from_transition.setdefault(transition_names[src], set()).add(tgt)
            print(f"miticooooooooooooooo",arcs_from_transition)
            #print("cazzolesso")
        if src in place_ids:
            arcs_from_place.setdefault(src, set()).add(transition_names[tgt])
            print(f"colioneee",transition_names[tgt])
            #print(arcs_from_place)
            #print("cazzolesso")
    # group arcs by target and source
    def find_non_silent_successors(silent, visited=None):
        if visited is None:
            visited = set()
        if silent in visited:
            return set()
        
        visited.add(silent)
       # print(visited)
        print("cazzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
        result = set()
        for place in arcs_from_transition.get(silent, []):
            for tr in arcs_from_place.get(place, []):
                if tr in silent_labels:
                    result |= find_non_silent_successors(tr, visited)
                else:
                    result.add(tr)
        print(result)    
        return result
            

    replacements = {silent: find_non_silent_successors(silent) for silent in silent_labels}
    #print(replacements)
    return replacements

# Apply replacements: per raw constraint, expand silent in preds and succs separately

def apply_replacements(altprec_constraints, replacements, silent_labels):
    """
    Substitute silent transitions with their immediate non-silent successors per place.
    Only generate constraints for:
    - case: silent in successors (split by each replacement)
    - case: no silent at all (keep original)
    """
    processed = []
    for constraint in altprec_constraints:
        pred, succ = constraint["parameters"]
        has_pred_silent = pred & silent_labels
        has_succ_silent = succ & silent_labels

        # Only handle successors-silent for closure
        if has_succ_silent:
            for s in has_succ_silent:
                for repl in replacements.get(s, []):
                    new_pred = pred - silent_labels
                    new_succ = (succ - {s}) | {repl}
                    if new_pred and new_succ and not new_pred & new_succ:
                        processed.append({
                            "template": "AlternatePrecedence",
                            "parameters": [new_pred, new_succ]
                        })
        # Keep original if no silents in either pred or succ
        elif not has_pred_silent and not has_succ_silent:
            processed.append(constraint)
    return processed


def get_alternate_precedence_with_closure(workflow_net):
    # Get the alternate precedence constraints
    altprec_constraints = get_alternate_precedence(workflow_net)
    # print("Raw Constraints:", altprec_constraints)
    silent_labels = {t["name"] for t in workflow_net["transitions"] if t.get("is_tau", False)}
    # print("Silent Labels:", silent_labels)
    replacements = compute_silent_replacements(workflow_net, silent_labels)
    # print("Replacements:", replacements)
    final = apply_replacements(altprec_constraints, replacements, silent_labels)
    # print("Final Constraints:", final)
    
    # convert sets to lists
    for c in final:
        c["parameters"] = [list(c["parameters"][0]), list(c["parameters"][1])]
    return final



################################################# MAIN

def translate_to_DEC(workflow_net, model_name):

    mapping = {}
    for t in workflow_net["transitions"]:
        id_ = t["id"]
        name = "tau" if t.get("is_tau", False) else t.get("name")
        mapping.setdefault(name, []).append(id_)

    tasks = [transition["name"] for transition in workflow_net["transitions"] if not transition["is_tau"]]

    end_constraint = get_end_constraint(workflow_net)
    alternate_precedence = get_alternate_precedence_with_closure(workflow_net) #w/transitive closure
    atmost1 = get_atmost1_constraint(workflow_net)

    constraints = []
    constraints.extend(end_constraint)
    constraints.extend(atmost1)
    constraints.extend(alternate_precedence)

    output = {
        "name": model_name,
        "transitionMap": mapping,
        "tasks": tasks,
        "constraints": constraints,
    }

    return output




#TODO: ADD A CSV DEEBUG EXPORT FEATURE 
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


