import pm4py
import graphviz
from automa import build_automaton_from_ts
from exporter import save_automaton_to_json
from exporter import save_automaton_to_dot

def main():
    # Read PetriNet from pnml 
    net, im, fm = pm4py.read_pnml("/Users/l2brb/Documents/main/DECpietro/test/PLG/test_xor/models/sample_xor_evo_cleaned_pm4py.pnml")
    
    # Convert PetriNet into reachability graph
    reach_graph = pm4py.convert_to_reachability_graph(net, im, fm)
    
    if reach_graph:
        print("REACHABILITY GRAPH GENERATED SUCCESSFULLY.")
        
        # Generate automaton from reachability graph
        automaton = build_automaton_from_ts(reach_graph)
        print("AUTOMATA GENERATED SUCCESSFULLY.")
        print(automaton)
        print(automaton.states)
        print(automaton.transitions)
        print(automaton.initial_state)
        print(automaton.final_states)


        save_automaton_to_json(automaton, '/Users/l2brb/Documents/main/DECpietro/automata/test/automaton_complete.json')
        save_automaton_to_dot(automaton, '/Users/l2brb/Documents/main/DECpietro/automata/test/automaton_complete.dot')


        with open('/Users/l2brb/Documents/main/DECpietro/automata/test/automaton_complete.dot', 'r') as file:
            dot_source = file.read()
        dot = graphviz.Source(dot_source)
        dot.view()

if __name__ == "__main__":
    main()