import sys
import time
import psutil
import os
from src import petri_parser
from src import dec_translator_target_ultimate as dec_translator
# from src import csv_exporter
from src import json_exporter
from src import wn_json

def main():
    if len(sys.argv) != 2:
        print("Usage: python main_test.py <pnml_file_path>")
        sys.exit(1)
    
    pnml_file_path = sys.argv[1]

    start_time = time.time()
    process = psutil.Process(os.getpid())
    

    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)

    if workflow_net:
        output = dec_translator.translate_to_DEC(workflow_net)
    
    # Mem Usage
    memory_usage = process.memory_info().rss / (1024 * 1024)  
    
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000  


    print(f"{pnml_file_path},{memory_usage:.2f},{execution_time_ms:.2f}")


