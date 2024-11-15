import pm4py
from pm4py.visualization.transition_system import visualizer as ts_visualizer



# Pnml Reader
net, im, fm = pm4py.read_pnml("/Users/l2brb/Documents/main/DECpietro/test/PLG/test_xor/models/sample_xor_evo_cleaned_pm4py.pnml")

# converts pnml to a reachability graph
reach_graph = pm4py.convert_to_reachability_graph(net, im, fm)

################################################################################################################ 


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

# View and export pdf
pm4py.view_transition_system(reach_graph, format='pdf')
pm4py.save_vis_transition_system(reach_graph, '/Users/l2brb/Documents/main/DECpietro/automata/test/reachability/complete_reachability.pdf')

exit()

############################################## REACHABILITY CHECK ##############################################


from pm4py.util import nx_utils
def check_source_and_sink_reachability(reach_graph, unique_source, unique_sink):
    """
    Checks reachability of the source and the sink place from all simulation nodes (places/transitions)
    of the Petri net"""










