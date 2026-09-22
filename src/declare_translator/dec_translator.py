"""The three-spell encoding of safe, sound workflow nets over transition IDs.

Names are display metadata: they never identify symbols in the specification.
Every transition is retained, including unnamed or invisible PNML transitions.
The three rules and their place-wise branching are unchanged.
"""


def get_atmost1_constraint(workflow_net):
    """At most one occurrence from the initial place's postset."""
    arc_targets = {arc["target"] for arc in workflow_net["arcs"]}
    arcs_by_source = {}
    for arc in workflow_net["arcs"]:
        arcs_by_source.setdefault(arc["source"], []).append(arc)

    transition_ids = {t["id"] for t in workflow_net["transitions"]}
    atmost1 = set()
    for place in workflow_net["places"]:
        if place["id"] not in arc_targets:
            for arc in arcs_by_source.get(place["id"], []):
                if arc["target"] in transition_ids:
                    atmost1.add(arc["target"])
    return [{"template": "Atmost1", "parameters": [sorted(atmost1)]}]


def get_end_constraint(workflow_net):
    """The last transition belongs to the final place's preset."""
    arc_sources = {arc["source"] for arc in workflow_net["arcs"]}
    arcs_by_target = {}
    for arc in workflow_net["arcs"]:
        arcs_by_target.setdefault(arc["target"], []).append(arc)

    transition_ids = {t["id"] for t in workflow_net["transitions"]}
    end = set()
    for place in workflow_net["places"]:
        if place["id"] not in arc_sources:
            for arc in arcs_by_target.get(place["id"], []):
                if arc["source"] in transition_ids:
                    end.add(arc["source"])
    return [{"template": "End", "parameters": [sorted(end)]}]


def get_alternate_precedence(workflow_net):
    """One branched AlternatePrecedence(preset, postset) per internal place."""
    transition_ids = {t["id"] for t in workflow_net["transitions"]}
    place_ids = {p["id"] for p in workflow_net["places"]}
    arcs_from_place, arcs_to_place = {}, {}
    for arc in workflow_net["arcs"]:
        source, target = arc["source"], arc["target"]
        if source in place_ids:
            arcs_from_place.setdefault(source, set()).add(target)
        if target in place_ids:
            arcs_to_place.setdefault(target, set()).add(source)

    constraints = []
    for place in workflow_net["places"]:
        if place.get("initialMarking") == "1" or place.get("finalMarking") == "1":
            continue
        predecessors = arcs_to_place.get(place["id"], set()) & transition_ids
        successors = arcs_from_place.get(place["id"], set()) & transition_ids
        if predecessors and successors:
            constraints.append({
                "template": "AlternatePrecedence",
                "parameters": [sorted(predecessors), sorted(successors)],
            })
    return constraints


def translate_to_DEC(workflow_net, model_name):
    """Encode a safe, sound WF net; safety and soundness are preconditions.

    The alphabet is T, not the image of T under an activity-label mapping.
    The output retains the existing name/tasks/constraints JSON schema.
    """
    constraints = []
    constraints.extend(get_end_constraint(workflow_net))
    constraints.extend(get_atmost1_constraint(workflow_net))
    constraints.extend(get_alternate_precedence(workflow_net))
    return {
        "name": model_name,
        "tasks": [t["id"] for t in workflow_net["transitions"]],
        "constraints": constraints,
    }
