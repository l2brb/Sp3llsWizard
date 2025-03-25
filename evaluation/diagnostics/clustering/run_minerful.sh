#!/bin/bash

# PATHS
XES_DIR='/home/l2brb/main/DECpietro/evaluation/conformance/clustering/slider_minerful_100'
MODEL_FILE='/home/l2brb/main/DECpietro/evaluation/conformance/clustering/BPIC15_5f_alpha.json'
OUTPUT_DIR='/home/l2brb/main/DECpietro/evaluation/conformance/clustering/output_minerful_100'
MINERFUL_DIR='/home/l2brb/main/MINERful' 
MINERFUL_SCRIPT='run-MINERfulFitnessChecker-unstable.sh'

# Creazione della cartella output se non esiste
mkdir -p "$OUTPUT_DIR"

# Loop su tutti i file .xes nella cartella XES_DIR
for xes_file in "$XES_DIR"/*.xes; do
    base_name=$(basename "$xes_file" .xes)
    output_csv="$OUTPUT_DIR/${base_name}.csv"

    # Stampa il comando prima di eseguirlo
    echo "Processing: $xes_file -> $output_csv"
    
    # Spostati nella cartella di MINERful ed esegui il comando
    (
        cd "$MINERFUL_DIR" || exit 1
        ./$MINERFUL_SCRIPT -iLE xes -iLF "$xes_file" -iSE json -iSF "$MODEL_FILE" -oCSV "$output_csv"
    )

    # Controlla se il file CSV è stato creato
    if [ -f "$output_csv" ]; then
        echo "Saved: $output_csv"
    else
        echo "Error: $output_csv NOT GENERATED!"
    fi

done

echo "DONE"
