#!/bin/bash

input_folder="/home/l2brb/main/DECpietro/evaluation/d_contraints/expanded_pnml/out-complete"
output_csv="/home/l2brb/main/DECpietro/evaluation/d_contraints/results/results_rog_dconstraints_updated_bugfix.csv"


echo "file_name,mem_usage_mb,peak_mem_mb,avg_mem_overall_mb,time_ms" > "$output_csv"


for file_path in $(ls "$input_folder" | sort); do
    full_path="$input_folder/$file_path"
    
    if [ -f "$full_path" ]; then

        
        output=$(python3 main.py "$full_path")

        
        memory_usage=$(echo "$output" | grep "Memory usage (rss)" | awk '{print $4}')
        peak_memory=$(echo "$output" | grep "Peak memory (tracemalloc)" | awk '{print $4}')
        avg_memory_overall=$(echo "$output" | grep "Average memory (overall)" | awk '{print $4}')
        execution_time=$(echo "$output" | grep "Execution time" | awk '{print $3}')

       
        file_name=$(basename "$file_path")

        
        echo "$file_name,$memory_usage,$peak_memory,$avg_memory_overall,$execution_time" >> "$output_csv"
        echo "Processed $file_name: Memory usage = $memory_usage MB, Peak memory = $peak_memory MB, Average memory (overall) = $avg_memory_overall MB, Execution time = $execution_time ms"
    fi
done

echo "Results saved in $output_csv"
