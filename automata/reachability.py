import pm4py
from pm4py.visualization.transition_system import visualizer as ts_visualizer



# Pnml Reader
net, im, fm = pm4py.read_pnml("/home/l2brb/main/DECpietro/test/PLG/test_and/and_pm4py.pnml")

# converts pnml to a reachability graph
reach_graph = pm4py.convert_to_reachability_graph(net, im, fm)
print("Stati del grafo di raggiungibilità:")
for state in reach_graph.states:
    print(f"Stato: {state}")
#print(reach_graph)

print("\nTransizioni del grafo di raggiungibilità:")
for transition in reach_graph.transitions:
    print(f"Transizione: {transition}")
gviz = ts_visualizer.apply(reach_graph)
ts_visualizer.view(gviz)

"""# Export pdf
ts_visualizer.save(
    gviz, "/Users/luca/Documents/^main/DECpietro/output/reach_graph_it.pdf"
    )
"""

exit()


############################################## DOT CONVERSION ##############################################


from graphviz import Digraph

# Funzione per esportare il reachability graph (transition system) in formato DOT
def export_reach_graph_to_dot(reach_graph, filename="reachability_graph.dot"):
    # Crea un grafo diretto (Digraph)
    dot = Digraph(comment='Reachability Graph')

    # Aggiungi i nodi (stati) al grafo
    for state in reach_graph.states:
        dot.node(str(state), str(state))  # Crea un nodo per ogni stato

    # Aggiungi le transizioni (archi) al grafo
    for (source, label, target) in reach_graph.transitions:
        dot.edge(str(source), str(target), label=str(label))  # Crea un arco con l'etichetta della transizione

    # Esporta il grafo in un file .dot
    dot.render(filename, format='dot')
    print(f"Reachability graph exported to {filename}")


# Esporta il reachability graph in formato DOT
export_reach_graph_to_dot(reach_graph)







