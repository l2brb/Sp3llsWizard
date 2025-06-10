import pm4py
import graphviz

with open('/home/l2brb/main/DECpietro/conformance/nfa_dfa/wn_nfa_automata_clean.dot', 'r') as file:
    dot_source = file.read()
dot = graphviz.Source(dot_source)
dot.view()