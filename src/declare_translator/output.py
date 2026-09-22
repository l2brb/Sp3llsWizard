"""Post-process an ID-based specification for export, without changing synthesis."""

from copy import deepcopy


def format_specification(specification, workflow_net, symbols="labels"):
    """Export IDs or substitute display labels after synthesis.

    Both modes retain transitionsMap (label -> IDs) for subsequent refinement.
    Label substitution is not a language-preserving projection in general when
    multiple transitions share a label. No silent transition is eliminated.
    """
    if symbols not in {"ids", "labels"}:
        raise ValueError("symbols must be 'ids' or 'labels'")

    id_to_label, transitions_map = {}, {}
    for transition in workflow_net["transitions"]:
        transition_id = transition["id"]
        name = transition.get("name")
        label = name if name and name.strip() else transition_id
        id_to_label[transition_id] = label
        transitions_map.setdefault(label, []).append(transition_id)

    output = deepcopy(specification)
    if symbols == "labels":
        def replace(ids):
            # Parameters and tasks are sets of symbols, serialized as lists.
            return list(dict.fromkeys(id_to_label[tid] for tid in ids))

        output["tasks"] = replace(output["tasks"])
        for constraint in output["constraints"]:
            constraint["parameters"] = [replace(group) for group in constraint["parameters"]]
    output["transitionsMap"] = transitions_map
    return output
