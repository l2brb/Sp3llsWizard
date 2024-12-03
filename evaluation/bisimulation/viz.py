import pm4py
import graphviz

with open('/home/l2brb/main/DECpietro/evaluation/bisimulation/reachability_graph/REVISED_targetsource.dot', 'r') as file:
    dot_source = file.read()
dot = graphviz.Source(dot_source)
dot.view()
