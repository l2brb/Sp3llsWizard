import pydot
from pyformlang.finite_automaton import FiniteAutomaton

DOT_NFA = "/home/l2brb/main/DECpietro/conformance/nfa_dfa/wn_nfa_automata_clean.dot"       
DOT_DFA = "/home/l2brb/main/DECpietro/conformance/nfa_dfa/wn_nfa_automata_clean._dfa.dot"  

# carica NFA dal .dot con pydot e pyformlang
graph, = pydot.graph_from_dot_file(DOT_NFA)
nfa = FiniteAutomaton.from_pydot(graph)

dfa = nfa.determinize()   #.minimize()   
with open(DOT_DFA, "w") as f:
    f.write(dfa.to_dot())

