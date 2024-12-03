import time
import psutil
import os
import sys
import tracemalloc
from src import petri_parser
from src import dec_translator_target_ultimate_update as dec_translator

def main():
    if len(sys.argv) < 2:
        print("Error: no PNML path")
        sys.exit(1)
    pnml_file_path = sys.argv[1]

    
    tracemalloc.start()
    memory_snapshots = []

    def capture_memory():
        current, _ = tracemalloc.get_traced_memory()
        memory_snapshots.append(current / (1024 * 1024))  

    start_time = time.time()  # TIME ##################################################
    process = psutil.Process(os.getpid())

    # mem iniziale
    capture_memory()

    # 1 petri_parser
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
    capture_memory()  

    model_name = os.path.basename(pnml_file_path)

    # 2 dec_translator
    if workflow_net:
        output = dec_translator.translate_to_DEC(workflow_net, model_name)
        capture_memory()  

    # mem finale
    capture_memory()

    # Mem Usage psutil
    memory_usage = process.memory_info().rss / (1024 * 1024)  # Converti in MB

    # tracemalloc
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # TIME ###########################################################################
    end_time = time.time() 
    execution_time_ms = (end_time - start_time) * 1000

    # mem tot tracemalloc
    avg_memory_overall = sum(memory_snapshots) / len(memory_snapshots) if memory_snapshots else 0

    print(f"Execution time: {execution_time_ms:.2f} ms")
    print(f"Memory usage (rss): {memory_usage:.2f} MB")
    print(f"Peak memory (tracemalloc): {peak / (1024 * 1024):.2f} MB")
    print(f"Average memory (overall): {avg_memory_overall:.2f} MB")



if __name__ == "__main__":
    main()
