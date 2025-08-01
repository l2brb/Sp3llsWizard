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
                # altrimenti qui si aggiungono i nomi delle transizioni
                #transition_name, is_tau = transition_by_id.get(transition_id, (None, False))


                # questo ce lo riprendiamo dopo

                # if is_tau:
                #     # if tau -> substitute with artificial "START"
                #     atmost1_constraints.add("START")
                # elif transition_name:
                #     atmost1_constraints.add(transition_name
                atmost1_constraints.add(trans_id)
    print(atmost1_constraints)                
    return [{
        "template": "Atmost1",
        "parameters": [list(atmost1_constraints)],   #TODO: CHECK DONE
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

                # altrimenti qui si aggiungono i nomi delle transizioni
                #transition_name, is_tau = transition_by_id.get(transition_id, (None, False))
                # #print(transition_name, is_tau)
                
                # if is_tau:
                #     end_constraints.add("END")
                # elif transition_name:
                #     end_constraints.add(transition_name)
                # #print(end_constraints)
                end_constraints.add(trans_id)
    print(end_constraints)                
    return [{
        "template": "End",
        "parameters": [list(end_constraints)], #TODO: CHECK DONE
    }]


# RELATION CONSTRAINTS

# Alternate Precedence [if B prev A and not B in between]
def get_alternate_precedence(workflow_net):
    # transition names mapping 
    transition_ids = {t["id"] for t in workflow_net["transitions"]} 
    # set of place IDs
    place_ids = {p["id"] for p in workflow_net["places"]}

    arcs_from_place, arcs_to_place = {}, {}

    # group arcs by source and target
    for arc in workflow_net["arcs"]:
        src, tgt = arc["source"], arc["target"]


        if src in place_ids:
            arcs_from_place.setdefault(src, set()).add(tgt)   # source -> target
        if tgt in place_ids:
            arcs_to_place.setdefault(tgt, set()).add(src)     # target -> source

    altprecedence_constraints = []

    for place in workflow_net["places"]:
        # salta place iniziale o finale
        if place.get("initialMarking") == "1" or place.get("finalMarking") == "1":
            continue

        preds = arcs_to_place.get(place["id"], set()) & transition_ids #intersection with transition IDs 
        succs = arcs_from_place.get(place["id"], set()) & transition_ids

        if preds and succs:
            altprecedence_constraints.append({
                "template": "AlternatePrecedence",
                "parameters": [list(preds), list(succs)]
            })

    print(altprecedence_constraints)
    return altprecedence_constraints

######################################################
def close_tau_stepwise(constraints, silent_ids):
    """
    Rimuove le transizioni silenti (τ) dai vincoli AlternatePrecedence
    senza fondere né inventare raggruppamenti branched.

    constraints  : lista di vincoli grezzi (template, parameters) in ID
    silent_ids   : set di ID silenti
    """
    # ----- copia mutabile dei parametri --------------------------------
    work = [
        {"template": c["template"],
         "parameters": [set(c["parameters"][0]), set(c["parameters"][1])]}
        for c in constraints
    ]

    # ----- grafo dei collegamenti τ → (altri τ o visibili) -------------
    forward = {tau: set() for tau in silent_ids}   # τ nel pred  → succ
    backward = {tau: set() for tau in silent_ids}  # τ nel succ → pred

    for c in work:
        P, S = c["parameters"]
        vis_S = S - silent_ids
        vis_P = P - silent_ids
        for tau in P & silent_ids:
            forward[tau] |= S                      # può includere τ
        for tau in S & silent_ids:
            backward[tau] |= P

    # transitive closure
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def forward_vis(tau):
        vis = set(x for x in forward[tau] if x not in silent_ids)
        for nxt in forward[tau] & silent_ids:
            vis |= forward_vis(nxt)
        return vis

    @lru_cache(maxsize=None)
    def backward_vis(tau):
        vis = set(x for x in backward[tau] if x not in silent_ids)
        for nxt in backward[tau] & silent_ids:
            vis |= backward_vis(nxt)
        return vis

    # substitutions
    for c in work:
        pred, succ = c["parameters"]

        # sostituisci τ nel succ (forward)
        for tau in set(succ) & silent_ids:
            succ.remove(tau)
            succ |= forward_vis(tau)

        # sostituisci τ nel pred (backward)
        for tau in set(pred) & silent_ids:
            pred.remove(tau)
            repl = backward_vis(tau)
            # tieni solo quelli che non violano pred∩succ = ∅
            pred |= (repl - succ)

    # serializations
    cleaned = []
    for c in work:
        p, s = map(list, c["parameters"])
        if p and s and set(p).isdisjoint(s):
            cleaned.append({"template": c["template"],
                            "parameters": [p, s]})
    return cleaned




########################################################### MAIN ##########################################################

# MAIN translate_to_DEC

def translate_to_DEC(workflow_net, model_name):
    
    mapping = {}
    for t in workflow_net["transitions"]:
        name = t.get("name")  # fallback a tau se name mancante
        id_ = t["id"]
        mapping.setdefault(name, []).append(id_)
    
    
    tasks = [transition["name"] for transition in workflow_net["transitions"] if not transition["is_tau"]]


    # Get constraints
    atmost1 = get_atmost1_constraint(workflow_net)
    end_constraint = get_end_constraint(workflow_net)
    alternate_precedence = get_alternate_precedence(workflow_net)

    #Apply closure on silent transitions
    # silent_ids = {t["id"] for t in workflow_net["transitions"] if t["is_tau"]}
    # alternate_precedence = close_tau_stepwise(alternate_precedence, silent_ids)


    constraints = []
    constraints.extend(end_constraint)
    constraints.extend(atmost1)
    constraints.extend(alternate_precedence)


    id2name = {tid: name for name, ids in mapping.items() for tid in ids}

    for c in constraints:
        new_params = []
        for param_list in c["parameters"]:
            new_params.append([id2name.get(x, x) for x in param_list])
        c["parameters"] = new_params

    output = {
        "name": model_name,
        "transitionsMap": mapping,
        "tasks": tasks,
        "constraints": constraints,
    }


    
    return output














