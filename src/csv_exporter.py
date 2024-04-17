"""

def write_to_csv(constraints):
    with open('/Users/luca/Documents/^main/DECpietro/output/constraints.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for key, value in constraints.items():
            writer.writerow([key, value])"""