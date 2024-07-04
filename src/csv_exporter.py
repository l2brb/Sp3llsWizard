import csv

def write_to_csv(constraints):
    with open('/home/l2brb/Docker/DECpietro/output/contraints_ln.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for key, value in constraints.items():
            writer.writerow([key, value])