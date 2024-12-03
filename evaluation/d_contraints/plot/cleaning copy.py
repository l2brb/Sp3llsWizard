import csv
import re

def clean_and_sort_csv(input_file, output_file):
    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    # Extract numbers from file_name and replace the file_name with the number
    for row in rows:
        match = re.search(r'^(\d+)\.pnml$', row['file_name'])
        if match:
            row['file_name'] = int(match.group(1))
        else:
            row['file_name'] = None  # Handle cases where the file_name does not match the pattern

    # Remove rows with None as file_name
    rows = [row for row in rows if row['file_name'] is not None]

    # Sort rows by the extracted file_number
    sorted_rows = sorted(rows, key=lambda x: x['file_name'])

    # Write the cleaned and sorted data to a new CSV file
    with open(output_file, mode='w', newline='') as outfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted_rows:
            writer.writerow(row)

if __name__ == "__main__":
    input_file = '/home/l2brb/main/DECpietro/evaluation/d_contraints/results/results_rog_dconstraints.csv'
    output_file = '/home/l2brb/main/DECpietro/evaluation/d_contraints/results/cleaned_results_rog_dconstraints.csv'
    clean_and_sort_csv(input_file, output_file)