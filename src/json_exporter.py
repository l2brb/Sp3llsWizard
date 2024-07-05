import json

def write_to_json(output):
    with open('/home/l2brb/Docker/DECpietro/output/contraints_ln.json', 'w') as file:
        json.dump(output, file)
        