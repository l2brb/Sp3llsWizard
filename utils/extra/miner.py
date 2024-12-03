import pm4py


# Read XES
event_log = pm4py.read_xes(
    '/home/l2brb/main/DECpietro/evaluation/conformance/real-world/bpic14f/BPIC14_f.xes'
    )
# # Discover the Petri net (Alpha Miner)
net, im, fm = pm4py.discover_petri_net_alpha(
    event_log)
# print(net)

# Discover the Petri net (Heuristics Miner)
# net, im, fm = pm4py.discover_petri_net_heuristics(
#     event_log)
# print(net)

# # Discover the Petri net (Inductive Miner)
# net, im, fm = pm4py.discover_petri_net_alpha(
#      event_log)
# #print(net)

"""# Discover the BPMN
bpmn_graph = pm4py.discover_bpmn_inductive(
    event_log)
# Visualize the bpmn
pm4py.view_bpmn(bpmn_graph, format='pdf')
pm4py.save_vis_bpmn(bpmn_graph, file_path='/home/l2brb/main/DECpietro/test/literature/RTFMP/RTFMP.pdf')
pm4py.write_bpmn(bpmn_graph, '/home/l2brb/main/DECpietro/test/literature/RTFMP/RTFMP.bpmn')"""


# Export to PNML
log = pm4py.write_pnml(net, im, fm, '/home/l2brb/main/DECpietro/evaluation/conformance/real-world/bpic14f/bpic14f_aplha.pnml')

# # Export pdf
pm4py.view_petri_net(net, im, fm, format='pdf')
pm4py.save_vis_petri_net(net, im, fm, file_path='/home/l2brb/main/DECpietro/evaluation/conformance/real-world/bpic14f/bpic14f_aplha.pdf')
