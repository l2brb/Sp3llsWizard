import pm4py


# Read XES
event_log = pm4py.read_xes(
    '/Users/luca/Documents/^main/DECpietro/petri_test/motivating_confine/pharma.xes'
    )

# Discover the Petri net
net, im, fm = pm4py.discover_petri_net_heuristics(
    event_log)
print(net)

print("######################################")

#Place
for plc in net.places:
    print((plc))
print("######################################")

#Transition

for trs in net.transitions:
    print((trs))
print("######################################")

#Arc
for arc in net.arcs:
    print((arc))
print("######################################")
