import pm4py
import graphviz

with open('/home/l2brb/main/DECpietro/automata/utils/lucaciao_provaaltrespinitend.dot', 'r') as file:
    dot_source = file.read()
dot = graphviz.Source(dot_source)
dot.view()
