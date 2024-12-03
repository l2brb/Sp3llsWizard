import pm4py
import graphviz
from automa import build_automaton_from_ts
from exporter import save_automaton_to_json
from exporter import save_automaton_to_dot

def main():
    # Read PetriNet from pnml 
    net, im, fm = pm4py.read_pnml("/home/l2brb/main/DECpietro/evaluation/bisimulation/reachability_graph/REVISED EASIER.pnml")
    
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


        save_automaton_to_json(automaton, '/home/l2brb/main/DECpietro/evaluation/bisimulation/reachability_graph/REVISED EASIER.json')
        save_automaton_to_dot(automaton, '/home/l2brb/main/DECpietro/evaluation/bisimulation/reachability_graph/REVISED EASIER.dot')


        with open('/home/l2brb/main/DECpietro/evaluation/bisimulation/reachability_graph/REVISED EASIER.dot', 'r') as file:
            dot_source = file.read()
        dot = graphviz.Source(dot_source)
        dot.view()

if __name__ == "__main__":
    main()