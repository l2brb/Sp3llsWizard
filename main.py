import time
import psutil
import os
import sys
from src import petri_parser
from src import dec_translator_target_ultimate as dec_translator

def main():
    # Verifica che sia stato passato un argomento per il file
    if len(sys.argv) < 2:
        print("Errore: specifica il percorso del file PNML come argomento.")
        sys.exit(1)

    # Prende il percorso del file PNML dalla riga di comando
    pnml_file_path = sys.argv[1]

    # Inizia a misurare tempo e memoria
    start_time = time.time()
    process = psutil.Process(os.getpid())
    
    # Esegue il parsing e la traduzione
    workflow_net = petri_parser.parse_wn_from_pnml(pnml_file_path)
    if workflow_net:
        output = dec_translator.translate_to_DEC(workflow_net)
    
    # Mem Usage
    memory_usage = process.memory_info().rss / (1024 * 1024)  
    print(f"Memory usage: {memory_usage:.2f} MB")

    # Execution Time
    end_time = time.time()
    execution_time_ms = (end_time - start_time) * 1000  
    print(f"Execution time: {execution_time_ms:.2f} ms")

if __name__ == "__main__":
    main()
