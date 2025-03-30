import json

def write_to_json(workflow_net, output_path):
    with open(output_path, 'w') as file:
        json.dump(workflow_net, file, indent=4)
