import pm4py

# Read xes file
event_log = pm4py.read_xes('your path')

# Discover the WF net (Inductive Miner)
net, im, fm = pm4py.discover_petri_net_alpha(
    event_log)
print(net)

# Export to PNML
log = pm4py.write_pnml(net, im, fm, 'your path')

# # Export pdf
pm4py.view_petri_net(net, im, fm, format='pdf')
pm4py.save_vis_petri_net(net, im, fm, file_path='your path')

exit()


"""

# Discover the Petri net (Alpha Miner)
net, im, fm = pm4py.discover_petri_net_alpha(
    event_log)
# print(net)

# Discover the Petri net (Heuristics Miner)
net, im, fm = pm4py.discover_petri_net_heuristics(
   event_log)
print(net)

# Discover the BPMN
bpmn_graph = pm4py.discover_bpmn_inductive(
    event_log)
# Visualize the bpmn
pm4py.view_bpmn(bpmn_graph, format='pdf')
pm4py.save_vis_bpmn(bpmn_graph, file_path='')
pm4py.write_bpmn(bpmn_graph, '')

"""



