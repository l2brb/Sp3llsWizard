import json

def write_to_json(output):
    with open('/home/l2brb/main/DECpietro/utils/Trules/T1a/t1prova', 'w') as file:
        json.dump(output, file)
        