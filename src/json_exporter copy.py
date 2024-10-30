import json

def write_to_json(output):
    with open('/home/l2brb/main/DECpietro/test/PLG/test_xor/xor_constraints.json', 'w') as file:
        json.dump(output, file)
        