#!/bin/bash

# Cartella di input e file CSV di output
input_folder="/Users/l2brb/Documents/main/DECpietro/utils/transition_only/linear"
output_csv="/Users/l2brb/Documents/main/DECpietro/evaluation/memory/results.csv"

# Intestazioni del file CSV
echo "file_name,mem_usage_mb,time_ms" > "$output_csv"

# Itera sui file nella cartella, ordinati alfabeticamente
for file_path in $(ls "$input_folder" | sort); do
    full_path="$input_folder/$file_path"
    
    # Controlla se è un file
    if [ -f "$full_path" ]; then
        # Esegui `main.py` con il file come argomento e cattura l'output
        output=$(python main.py "$full_path")

        # Estrai i valori di memoria e tempo di esecuzione dall'output di `main.py`
        memory_usage=$(echo "$output" | grep "Memory usage" | awk '{print $3}')
        execution_time=$(echo "$output" | grep "Execution time" | awk '{print $3}')

        # Estrai il nome del file dal percorso
        file_name=$(basename "$file_path")

        # Salva i risultati nel file CSV
        echo "$file_name,$memory_usage,$execution_time" >> "$output_csv"
    fi
done

echo "results in $output_csv"
