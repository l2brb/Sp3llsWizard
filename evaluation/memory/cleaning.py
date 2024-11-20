import csv
import re

def clean_and_sort_csv(input_file, output_file):
    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    # Extract numbers from file_name after the last underscore and replace the file_name with the number
    for row in rows:
        match = re.search(r'_(\d+)\.pnml$', row['file_name'])
        if match:
            row['file_name'] = int(match.group(1))

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
    input_file = '/home/l2brb/main/DECpietro/evaluation/memory/results_rog_t1-2a.csv'
    output_file = '/home/l2brb/main/DECpietro/evaluation/memory/cleaned_results_rog_t1-2a.csv'
    clean_and_sort_csv(input_file, output_file)