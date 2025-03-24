import json

def write_to_json(workflow_net):
    with open('/home/l2brb/Docker/DECpietro/output/wn_ln.json', 'w') as file:
        json.dump(workflow_net, file)
        