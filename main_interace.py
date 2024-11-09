from src import petri_parser
from src import dec_translator_target_ultimate as dec_translator
from src import json_exporter
from src import csv_exporter
from src import wn_json  

def export_workflow_net(workflow_net, output_format):
    path = input("Enter the path ").strip()
    if output_format == "json":
        wn_json.write_to_json(workflow_net, path)
    elif output_format == "csv":
        csv_exporter.write_to_csv(workflow_net, path)

def generate_declare_constraints(workflow_net, output_format):
    output = dec_translator.translate_to_DEC(workflow_net)
    print("DECLARE constraints generated successfully.")
    path = input("Enter the path: ").strip()
    if output_format == "json":
        json_exporter.write_to_json(output, path)
    elif output_format == "csv":
        csv_exporter.write_to_csv(output, path)

def display_menu():
    """Displays the available operations menu and returns the user's choice."""
    print("\nSelect an operation:")
    print("1. Export Workflow net")
    print("2. Generate DECLARE constraints")
    print("3. Exit")
    return input("Enter the number of the operation you want to perform: ").strip()

def main():
    pnml_file_path = input("Enter the PNML file path for the Workflow net: ").strip()
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)

    if not workflow_net:
        print("Error: could not parse the WN.")
        return

    print("WORKFLOW NET PARSED SUCCESSFULLY.")

    while True:
        choice = display_menu()

        if choice == "1":
            output_format = input("Select the output format for the WN (json/csv): ").strip().lower()
            if output_format in ["json", "csv"]:
                export_workflow_net(workflow_net, output_format)
            else:
                print("Invalid format. Please try again.")

        elif choice == "2":
            output_format = input("Select the output format for the DECLARE constraints (json/csv): ").strip().lower()
            if output_format in ["json", "csv"]:
                generate_declare_constraints(workflow_net, output_format)
            else:
                print("Invalid format. Try again.")

        elif choice == "3":
            print("Exit.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
