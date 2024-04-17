import pm4py


# Read XES
event_log = pm4py.read_xes(
    '/Users/luca/Documents/^main/DECpietro/test/bpic12/log/BPI_Challenge_2012.xes'
    )

"""# Discover the Petri net (Heuristics Miner)
net, im, fm = pm4py.discover_petri_net_heuristics(
    event_log)
print(net)"""

# # Discover the Petri net (Alpha Miner)
# net, im, fm = pm4py.discover_petri_net_alpha(
#     event_log)
# print(net)

# Discover the Petri net (Inductive Miner)
net, im, fm = pm4py.discover_petri_net_inductive(
    event_log)
print(net)

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



# Export to PNML
log = pm4py.write_pnml(net, im, fm, '/Users/luca/Documents/^main/DECpietro/test/bpic12/bpic12_inductive.pnml')

# Export pdf
# pm4py.view_petri_net(net, im, fm, format='pdf')
pm4py.save_vis_petri_net(net, im, fm, file_path='/Users/luca/Documents/^main/DECpietro/test/bpic12/bpic12_inductive.pdf')
