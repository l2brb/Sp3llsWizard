import pm4py
from pm4py.visualization.transition_system import visualizer as ts_visualizer

#PNML READER
net, im, fm, = pm4py.read_pnml("/home/l2brb/main/DECpietro/utils/Trules/T5a/T5a_augmented_1.pnml", True)

#print(net, im, fm)



#export_pm4py_pnml = pm4py.write_pnml(net, im, fm, "/home/l2brb/main/DECpietro/utils/simple-wn-pm4py.pnml")
pm4py.view_petri_net(net, im, fm, format='pdf')

exit()


reach_graph = pm4py.convert_to_reachability_graph(net, im, fm)

print(reach_graph)


# gviz = ts_visualizer.apply(reach_graph)
# ts_visualizer.view(gviz)

# bpmn_graph = pm4py.convert_to_bpmn(net, im, fm)
# pm4py.view_petri_net(bpmn_graph, format='pdf')


# bpmn = pm4py.read_bpmn('/Users/luca/Documents/^main/DECpietro/test/PLG/new/1./2./bpmn_test_plg.bpmn')
# pm4py.view_petri_net(bpmn, format='pdf')