import time
import psutil
import os
from utils import petri_parser
from . import dec_translator_performance_test as dec_translator
from utils import json_exporter
from memory_profiler import profile



#@profile
def main():
    
    
    pnml_file_path = "/home/l2brb/main/DECpietro/evaluation/n_constraints/expanded_pnml/out-complete/999.pnml"
    
    # Execution Time
    start_time = time.time()
    process = psutil.Process(os.getpid())
    

    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
    if workflow_net:
        model_name = os.path.basename(pnml_file_path)
        output = dec_translator.translate_to_DEC(workflow_net, model_name)
    
    # Mem Usage
    memory_usage = process.memory_info().rss / (1024 * 1024) 
    
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000  

    #json_exporter.write_to_json(output)

    print(f"{memory_usage:.2f},{execution_time_ms:.2f}")

if __name__ == "__main__":
    main()


