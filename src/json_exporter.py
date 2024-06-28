import json

def write_to_json(constraints):
    with open('/Users/luca/Documents/^main/DECpietro/output/constraints.json', 'w') as file:
        json.dump(constraints, file)
        