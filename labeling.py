import pydot
from src.utils import petri_parser

DFA_IDS_DOT   = "/home/l2brb/main/DECpietro/conformance/nfa_dfa/wn_nfa_automata.dot"     # automa
DFA_LABEL_DOT = "/home/l2brb/main/DECpietro/conformance/nfa_dfa/wn_nfa_automata_clean.dot"  # output
PNML_FILE     = "/home/l2brb/main/DECpietro/conformance/wn_nfa.pnml"         # WF net


# mapping id/label
wf = petri_parser.parse_wn_from_pnml(PNML_FILE)
id2label = {t["id"]: t["name"] for t in wf["transitions"]}

# dot read
graph, = pydot.graph_from_dot_file(DFA_IDS_DOT)

# substitute labels
for edge in graph.get_edges():
    raw = edge.get_label()        
    if raw is None:
        continue                  
    tid = raw.strip('"')
    edge.set_label(id2label.get(tid, tid))

# export
graph.write(DFA_LABEL_DOT, format='raw')
