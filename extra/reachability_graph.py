import pm4py
from pm4py.visualization.transition_system import visualizer as ts_visualizer


# Pnml Reader
net, im, fm = pm4py.read_pnml("/Users/luca/Documents/^main/DECpietro/test/hospital.pnml")

# converts pnml to a reachability graph
reach_graph = pm4py.convert_to_reachability_graph(net, im, fm)
#print(type(reach_graph))


gviz = ts_visualizer.apply(reach_graph)
ts_visualizer.view(gviz)

"""# Export pdf
ts_visualizer.save(
    gviz, "/Users/luca/Documents/^main/DECpietro/output/reach_graph_it.pdf"
    )
"""