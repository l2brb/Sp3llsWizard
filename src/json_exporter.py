import json

def write_to_json(output):
    with open('/home/l2brb/main/DECpietro/test/PLG/test_and/target_branch/prova_real_constraints.json', 'w') as file:
        json.dump(output, file)
        