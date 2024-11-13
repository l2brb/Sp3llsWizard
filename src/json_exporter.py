import json

def write_to_json(output):
    with open('//Users/l2brb/Documents/main/DECpietro/test/PLG/test_xor/models/sample_xor_evo_cleaned.json', 'w') as file:
        json.dump(output, file)
        