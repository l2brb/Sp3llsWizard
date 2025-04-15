import pm4py
import graphviz
from evaluation.bisimulation.automa import build_automaton_from_ts
from exporter import save_automaton_to_json
from exporter import save_automaton_to_dot


# Pnml Reader
net, im, fm = pm4py.read_pnml('your_path')

# Reachability graph
reach_graph = pm4py.convert_to_reachability_graph(net, im, fm)

print("Reachability states:")
for state in reach_graph.states:
    print(f"State: {state}")

print("\nReachability transitions:")
for transition in reach_graph.transitions:
    print(f"Transition: {transition}")


print("\n")

for state in reach_graph.states:
    print(f"State {state.name} data:")
    print(state.name) 

# View and pdf export
pm4py.view_transition_system(reach_graph, format='pdf')
pm4py.save_vis_transition_system(reach_graph, 'your path')




def main():

    # WF pnml reader
    net, im, fm = pm4py.read_pnml('your_path')
    
    # Reachability graph conversion
    reach_graph = pm4py.convert_to_reachability_graph(net, im, fm)

    # print("Reachability states:")
    # for state in reach_graph.states:
    #     print(f"State: {state}")

    # print("\nReachability transitions:")
    # for transition in reach_graph.transitions:
    #     print(f"Transition: {transition}")


    # print("\n")

    # for state in reach_graph.states:
    #     print(f"State {state.name} data:")
    #     print(state.name) 

    # # View and pdf export
    # pm4py.view_transition_system(reach_graph, format='pdf')
    # pm4py.save_vis_transition_system(reach_graph, 'your path')
        
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


        save_automaton_to_json(automaton, 'your_path')
        save_automaton_to_dot(automaton, 'your_path')


        with open('your path', 'r') as file:
            dot_source = file.read()
        dot = graphviz.Source(dot_source)
        dot.view()



if __name__ == "__main__":
    main()