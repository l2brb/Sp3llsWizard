"""Independent finite-state oracle used only in tests.

Explore the full reachable product of the Petri marking automaton and the
DECLARE monitors. A mismatch yields a shortest distinguishing trace. There is
no trace-length cutoff: loops are handled by visiting each product state once.
"""

from collections import deque


def make_net(flows, labels=None):
    """Build a test net from transition -> (input places, output places)."""
    labels = labels or {}
    place_ids = sorted({p for ins, outs in flows.values() for p in ins + outs})
    arcs = []
    for transition, (inputs, outputs) in flows.items():
        arcs.extend({"source": p, "target": transition} for p in inputs)
        arcs.extend({"source": transition, "target": p} for p in outputs)
    targets, sources = {a['target'] for a in arcs}, {a['source'] for a in arcs}
    places = []
    for p in place_ids:
        item = {"id": p, "name": p, "initialMarking": "1" if p not in targets else "0"}
        if p not in sources:
            item['finalMarking'] = '1'
        places.append(item)
    return {
        "places": places,
        "transitions": [{"id": t, "name": labels.get(t, t)} for t in flows],
        "arcs": arcs,
    }


def monitor_step(constraints, state, event):
    if state is None:
        return None
    updated = []
    for constraint, previous in zip(constraints, state):
        template, params = constraint['template'], constraint['parameters']
        if template == 'End':
            current = event in params[0]
        elif template == 'Atmost1':
            if previous and event in params[0]:
                return None
            current = previous or event in params[0]
        elif template == 'AlternatePrecedence':
            predecessors, successors = params
            if event in successors and not previous:
                return None
            # A transition may consume and produce a token in the same place.
            current = event in predecessors or (previous and event not in successors)
        else:
            raise AssertionError(f'Unknown template: {template}')
        updated.append(current)
    return tuple(updated)


def monitor_accepts(constraints, state):
    return state is not None and all(
        value for c, value in zip(constraints, state) if c['template'] == 'End'
    )


def accepts(specification, trace):
    state = (False,) * len(specification['constraints'])
    for event in trace:
        if event not in specification['tasks']:
            return False
        state = monitor_step(specification['constraints'], state, event)
    return monitor_accepts(specification['constraints'], state)


def assert_equivalent(case, net, specification, max_states=100000):
    places = [p['id'] for p in net['places']]
    alphabet = tuple(t['id'] for t in net['transitions'])
    case.assertEqual(set(alphabet), set(specification['tasks']))
    initial = tuple(int(p.get('initialMarking') or 0) for p in net['places'])
    final = tuple(int(p.get('finalMarking') or 0) for p in net['places'])
    inputs = {t: {a['source'] for a in net['arcs'] if a['target'] == t} for t in alphabet}
    outputs = {t: {a['target'] for a in net['arcs'] if a['source'] == t} for t in alphabet}

    def fire(marking, event):
        if marking is None:
            return None
        tokens = dict(zip(places, marking))
        if any(tokens[p] == 0 for p in inputs[event]):
            return None
        result = tuple(tokens[p] - (p in inputs[event]) + (p in outputs[event]) for p in places)
        case.assertTrue(all(0 <= n <= 1 for n in result), 'Oracle fixture is not safe')
        return result

    constraints = specification['constraints']
    start = (initial, (False,) * len(constraints))
    pending, visited = deque([(start, ())]), {start}
    while pending:
        (marking, state), trace = pending.popleft()
        case.assertEqual(marking == final, monitor_accepts(constraints, state),
                         f'Distinguishing transition trace: {trace}')
        for event in alphabet:
            successor = (fire(marking, event), monitor_step(constraints, state, event))
            if successor not in visited:
                visited.add(successor)
                case.assertLessEqual(len(visited), max_states, 'Oracle state budget exceeded')
                pending.append((successor, trace + (event,)))
    return len(visited)
