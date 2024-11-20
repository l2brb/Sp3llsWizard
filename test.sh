#!/bin/bash


input_folder="/home/l2brb/main/DECpietro/utils/DTRules/out"
output_csv="/home/l2brb/main/DECpietro/evaluation/memory/results_rog_t1-2a.csv"

# CSV
echo "file_name,mem_usage_mb,time_ms" > "$output_csv"

# Itera sui file nella cartella, ordinati alfabeticamente
for file_path in $(ls "$input_folder" | sort); do
    full_path="$input_folder/$file_path"
    
    
    if [ -f "$full_path" ]; then

        output=$(python3 main.py "$full_path")

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
