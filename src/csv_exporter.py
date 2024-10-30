import csv

def write_to_csv(constraints, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        for key, value in constraints.items():
            writer.writerow([key, value])
    print(f"csv successfully exported to {path}")