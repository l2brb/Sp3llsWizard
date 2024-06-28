import pm4py

# imports a process tree from a PTML file
#bpmn = pm4py.read_bpmn('/Users/luca/Documents/^main/DECpietro/test/PLG/easy_test_1_bpmn.bpmn')

pnml = pm4py.read_pnml('/Users/luca/Documents/^main/DECpietro/test/PLG/easy_test_1.pnml')
pm4py.view_petri_net(pnml)

exit()


# print(bpmn)
# Visualize the bpmn
pm4py.view_bpmn(bpmn, format='pdf')
#pm4py.save_vis_bpmn(bpmn_graph, file_path='/Users/luca/Documents/^main/TEExProcessMining/models/bpmn.pdf')

# net, im, fm = pm4py.convert_to_petri_net(bpmn)

# print(net, im, fm)