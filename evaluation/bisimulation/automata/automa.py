import pm4py

class Automaton:
    def __init__(self):
        self.states = set()  # Q
        self.transitions = {}  # Funzione di transizione (stato, input) -> stato
        self.initial_state = None  # q_0
        self.final_states = set()  # Stati finali

    def add_state(self, state, is_initial=False, is_final=False):
        self.states.add(state)
        if is_initial:
            self.initial_state = state
        if is_final:
            self.final_states.add(state)

    def add_transition(self, from_state, to_state, action):
        if (from_state, action) not in self.transitions:
            self.transitions[(from_state, action)] = to_state
        else:
            raise Exception(f"Transition already defined for {(from_state, action)}")

    def get_next_state(self, current_state, action):
        return self.transitions.get((current_state, action), None)

    def is_final_state(self, state):
        return state in self.final_states


######################################### AUTOMATON FORM REACHABILITY GRAPH #########################################

def build_automaton_from_ts(reach_graph):
    automaton = Automaton()

    # INITIAL STATE
    states_with_incoming_transitions = {transition.to_state for transition in reach_graph.transitions}
    initial_state = next(state for state in reach_graph.states if state not in states_with_incoming_transitions)

    # FINAL STATE
    states_with_outgoing_transitions = {transition.from_state for transition in reach_graph.transitions}
    final_state = next(state for state in reach_graph.states if state not in states_with_outgoing_transitions)

    for state in reach_graph.states:
        is_initial = state == initial_state
        is_final = state == final_state
        automaton.add_state(state.name, is_initial=is_initial, is_final=is_final)

    for transition in reach_graph.transitions:
        from_state = transition.from_state.name  
        to_state = transition.to_state.name     
        action = transition.name                 
        
        automaton.add_transition(from_state, to_state, action)

    return automaton