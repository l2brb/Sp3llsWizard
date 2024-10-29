import pm4py
import graphviz

with open('/home/l2brb/main/DECpietro/test/PLG/test_xor/minerful_out/xor_constraints_full.dot', 'r') as file:
    dot_source = file.read()
dot = graphviz.Source(dot_source)
dot.view()
