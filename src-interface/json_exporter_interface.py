import json

def write_to_json(output, path):
    with open(path, 'w') as file:
        json.dump(output, file)
    print(f"JSON file successfully exported to {path}")