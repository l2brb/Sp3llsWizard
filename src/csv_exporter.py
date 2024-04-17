"""import csv
import dec_translator_splitted
import extra.old.petri_parser as petri_parser

def write_to_csv(constraint_name, activity_name):
    with open('constraints.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Constraint", "Activity"])
        writer.writerow([constraint_name, activity_name])

# Uso della funzione
constraint = "Init"
activity = dec_translator_splitted.get_init_constraint(workflow_net)
write_to_csv(constraint, activity)"""