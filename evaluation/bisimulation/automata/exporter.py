import json

######################################## JSON Exporter ########################################

def automaton_to_dict(automaton):
    alphabet = set(action for _, action in automaton.transitions.keys())
    transitions = [[from_state, action, to_state] for (from_state, action), to_state in automaton.transitions.items()]
    return {
        "alphabet": list(alphabet),
        "states": list(automaton.states),
        "initial_states": [automaton.initial_state] if automaton.initial_state else [],
        "accepting_states": list(automaton.final_states),
        "transitions": transitions
    }

def save_automaton_to_json(automaton, file_path):
    automaton_dict = automaton_to_dict(automaton)
    with open(file_path, 'w') as json_file:
        json.dump(automaton_dict, json_file, indent=2)


######################################## DOT Exporter ########################################

def automaton_to_dot(automaton):
    lines = ["digraph {"]
    
    # Initial State
    lines.append('  fake [style=invisible]')
    if automaton.initial_state:
        lines.append(f'  fake -> {automaton.initial_state} [style=bold]')
    
    # States
    for state in automaton.states:
        shape = "doublecircle" if state == automaton.final_states else "circle"
        lines.append(f'  {state} [shape={shape}]')
    
    # ATransitions
    for (from_state, action), to_state in automaton.transitions.items():
        lines.append(f'  {from_state} -> {to_state} [label="{action}"]')
    
    lines.append("}")
    return "\n".join(lines)

def save_automaton_to_dot(automaton, file_path):
    dot_representation = automaton_to_dot(automaton)
    with open(file_path, 'w') as dot_file:
        dot_file.write(dot_representation)