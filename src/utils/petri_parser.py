"""Read ordinary PNML workflow nets without projecting transition labels.

Validate the WF-net structure and boundary markings. Safety and soundness are
semantic preconditions of the encoding and are not decided by this parser.
"""

from lxml import etree


def _count(text, description):
    try:
        value = int(text)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid {description}: {text!r}") from exc
    if value < 0:
        raise ValueError(f"Negative {description}: {value}")
    return value


def _reachable(start, edges):
    visited, pending = set(), [start]
    while pending:
        node = pending.pop()
        if node not in visited:
            visited.add(node)
            pending.extend(edges.get(node, ()))
    return visited


def parse_wn_from_pnml(file_path):
    """Return places, transitions and arcs; IDs are preserved verbatim.

    Missing display names fall back to the node ID. Invisible transitions are
    ordinary alphabet symbols too; no transition is hidden or bypassed.
    Malformed or unsupported inputs raise an exception instead of producing an
    incomplete specification. Missing boundary markings are inferred from the
    unique source and sink, as prescribed by the WF-net definition.
    """
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    root = etree.parse(str(file_path), parser).getroot()
    # PNML documents occur both with and without a default XML namespace.
    for element in root.iter():
        if isinstance(element.tag, str):
            element.tag = etree.QName(element).localname
    nets = root.findall('.//net')
    if root.tag != 'pnml' or len(nets) != 1:
        raise ValueError("Expected a PNML document containing exactly one net")
    net = nets[0]
    if net.findall('.//referencePlace') or net.findall('.//referenceTransition'):
        raise ValueError("PNML reference nodes are not supported")

    workflow_net = {"places": [], "transitions": [], "arcs": []}
    node_ids = set()
    initial = {}
    explicit_initial = False
    for kind, collection in (("place", "places"), ("transition", "transitions")):
        for node in net.findall(f'.//{kind}'):
            # finalmarkings/place is a marking reference, not a graph node.
            if kind == "place" and node.getparent().tag == "marking":
                continue
            node_id = node.get("id")
            if not node_id or node_id in node_ids:
                raise ValueError(f"Missing or duplicate node ID: {node_id!r}")
            node_ids.add(node_id)
            name = node.findtext('name/text')
            item = {"id": node_id, "name": name if name and name.strip() else node_id}
            if kind == "place":
                mark = node.find('initialMarking')
                if mark is not None:
                    explicit_initial = True
                    initial[node_id] = _count(mark.findtext('text'), "initial marking")
                item["initialMarking"] = str(initial.get(node_id, 0))
            workflow_net[collection].append(item)

    places = {p["id"] for p in workflow_net["places"]}
    transitions = {t["id"] for t in workflow_net["transitions"]}
    if not places or not transitions:
        raise ValueError("A workflow net must contain places and transitions")
    forward, backward, seen_arcs = {}, {}, set()
    for arc in net.findall('.//arc'):
        source, target = arc.get("source"), arc.get("target")
        if not ((source in places and target in transitions)
                or (source in transitions and target in places)):
            raise ValueError(f"Invalid or dangling bipartite arc: {source!r} -> {target!r}")
        weight = _count(arc.findtext('inscription/text', default='1'), "arc weight")
        arc_type = arc.find('type')
        if weight != 1 or (arc_type is not None and arc_type.get('value') != 'normal'):
            raise ValueError("Only ordinary, unit-weight arcs are supported")
        if (source, target) in seen_arcs:
            raise ValueError(f"Duplicate arc: {source!r} -> {target!r}")
        seen_arcs.add((source, target))
        forward.setdefault(source, set()).add(target)
        backward.setdefault(target, set()).add(source)
        workflow_net["arcs"].append({"source": source, "target": target})

    sources, sinks = places - backward.keys(), places - forward.keys()
    if len(sources) != 1 or len(sinks) != 1:
        raise ValueError("Expected exactly one source place and one sink place")
    source, sink = next(iter(sources)), next(iter(sinks))
    if _reachable(source, forward) != node_ids or _reachable(sink, backward) != node_ids:
        raise ValueError("Every node must lie on a path from the source to the sink")
    if explicit_initial and {p: n for p, n in initial.items() if n} != {source: 1}:
        raise ValueError("The initial marking must contain one token in the source only")

    final = net.find('finalmarkings')
    if final is not None:
        markings = final.findall('marking')
        if len(markings) != 1:
            raise ValueError("Expected exactly one final marking")
        final_counts = {}
        for place in markings[0].findall('place'):
            place_id = place.get('idref')
            if place_id not in places or place_id in final_counts:
                raise ValueError(f"Invalid final-marking reference: {place_id!r}")
            final_counts[place_id] = _count(place.findtext('text'), "final marking")
        if {p: n for p, n in final_counts.items() if n} != {sink: 1}:
            raise ValueError("The final marking must contain one token in the sink only")

    for place in workflow_net["places"]:
        place["initialMarking"] = "1" if place["id"] == source else "0"
        if place["id"] == sink:
            place["finalMarking"] = "1"
    return workflow_net
