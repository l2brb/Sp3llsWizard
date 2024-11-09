#!/bin/bash

# Directory contenente i file PNML
PNML_DIR="/home/l2brb/main/DECpietro/utils/places_only/finegrade/"

# Percorso allo script Python
PYTHON_SCRIPT="/home/l2brb/main/DECpietro/main_test.py"

# File CSV per salvare i risultati
RESULTS_CSV="/home/l2brb/main/DECpietro/evaluation/results.csv"

# Scrivi l'intestazione del file CSV
echo "pnml_file,mem_usage_mb,execution_time_ms" > "$RESULTS_CSV"

# Itera attraverso tutti i file PNML nella directory
for pnml_file in "$PNML_DIR"/*.pnml; do
    echo "Eseguendo test per il file: $pnml_file"
    
    # Esegui lo script Python con il percorso del file PNML come argomento e cattura l'output
    result=$(/home/l2brb/miniconda3/envs/decpietro/bin/python "$PYTHON_SCRIPT" "$pnml_file")
    
    # Stampa di debug per verificare l'output catturato
    echo "Risultato catturato: $result"
    
    # Scrivi il risultato nel file CSV
    echo "$result" >> "$RESULTS_CSV"
    
    echo "Test completato per il file: $pnml_file"
    echo "----------------------------------------"
done