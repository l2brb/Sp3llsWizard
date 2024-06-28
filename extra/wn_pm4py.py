import pm4py


# Read XES
event_log = pm4py.read_xes(
    '/Users/luca/Documents/^main/DECpietro/test/italian/italian_help_desk.xes'
    )

# Discover the Petri net (Heuristics Miner)
net, im, fm = pm4py.discover_petri_net_heuristics(
    event_log)
# print(net)

# # Discover the Petri net (Alpha Miner)
#net, im, fm = pm4py.discover_petri_net_alpha(
#    event_log)
# print(net)

# Discover the Petri net (Inductive Miner)
#net, im, fm = pm4py.discover_petri_net_inductive(
#    event_log)
#print(net)

# print("######################################")

# #Place
# for plc in net.places:
#     print((plc))
# print("######################################")

# #Transition

# for trs in net.transitions:
#     print((trs))
# print("######################################")

# #Arc
# for arc in net.arcs:
#     print((arc))
# print("######################################")


"""# Discover the BPMN
bpmn_graph = pm4py.discover_bpmn_inductive(
    event_log)
# Visualize the bpmn
pm4py.view_bpmn(bpmn_graph, format='pdf')
#pm4py.save_vis_bpmn(bpmn_graph, file_path='/Users/luca/Documents/^main/TEExProcessMining/models/bpmn.pdf')
"""


# Export to PNML
log = pm4py.write_pnml(net, im, fm, '/Users/luca/Documents/^main/DECpietro/test/italian/italian_heuristics.pnml')

# Export pdf
# pm4py.view_petri_net(net, im, fm, format='pdf')
pm4py.save_vis_petri_net(net, im, fm, file_path='/Users/luca/Documents/^main/DECpietro/test/italian/italian_heuristics.pdf')
