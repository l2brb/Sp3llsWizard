import json

def write_to_json(constraints):
    with open('/home/l2brb/Docker/DECpietro/output/contraints_ln.json', 'w') as file:
        json.dump(constraints, file)
        