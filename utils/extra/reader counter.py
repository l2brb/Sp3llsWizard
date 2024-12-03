import os
import pm4py
import csv

directory = "/home/l2brb/main/DECpietro/evaluation/d_contraints/expanded_pnml/out-complete"

output_csv = "/home/l2brb/main/DECpietro/evaluation/d_contraints/expanded_pnml/stats_summary.csv"

results = []


for filename in os.listdir(directory):
    if filename.endswith(".pnml"):
        filepath = os.path.join(directory, filename)
        try:
           
            net, im, fm = pm4py.read_pnml(filepath)
            # pm4py.view_petri_net(net, im, fm, format='pdf')

            # Transitions
            num_transitions = len(net.transitions)
            # print(f"{num_transitions}")

            # Places
            num_places = len(net.places)
            # print(f"{num_places}")

            # keeping nodes
            nodes = set()

            for arc in net.arcs:
                source = arc.source
                target = arc.target
                node = (id(source), id(arc), id(target))
                nodes.add(node)

            num_nodes = len(nodes)
            # print(f"{num_nodes}")

            
            results.append({
                'filename': filename,
                'transitions': num_transitions,
                'places': num_places,
                'nodes': num_nodes
            })

        except Exception as e:
            print(f"Errore durante l'elaborazione del file {filename}: {e}")


with open(output_csv, mode='w', newline='') as csv_file:
    fieldnames = ['filename', 'transitions', 'places', 'nodes']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for result in results:
        writer.writerow(result)


