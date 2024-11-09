import time 
import psutil
import os
from src import petri_parser
from src import dec_translator_target_ultimate as dec_translator
# from src import csv_exporter
from src import json_exporter
from src import wn_json

def main():
    start_time = time.time()
    process = psutil.Process(os.getpid())
    pnml_file_path = "/home/l2brb/main/DECpietro/utils/places_only/finegrade/xor_pm4py_augmented_10000.pnml"
    
    
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
    if workflow_net:
        output = dec_translator.translate_to_DEC(workflow_net)
    
    # Mem Usage
    memory_usage = process.memory_info().rss / (1024 * 1024)  
    print(f"Memory usage: {memory_usage:.2f} MB")

    # Time
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000  
    print(f"Execution time: {execution_time_ms:.2f} ms")

if __name__ == "__main__":
    main()
