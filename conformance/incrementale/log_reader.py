import pm4py

LOG_PATH = "/home/l2brb/main/DECpietro/evaluation/performance/realworld/logs/sepsis/sepsis.xes"        
log = pm4py.read_xes(LOG_PATH)          



def extract_labels(trace, attribute="concept:name"):
    # Se la traccia è un dizionario e contiene la chiave "event", itera sugli eventi
    if isinstance(trace, dict) and "event" in trace:
        return [evt.get(attribute) if isinstance(evt, dict) else evt for evt in trace["event"]]
    # Altrimenti, per ogni elemento della traccia controlla se è un dizionario
    return [evt.get(attribute) if isinstance(evt, dict) else evt for evt in trace]

# Aggiunta del print per "concept:name" di ogni traccia
for trace in log:
    labels = extract_labels(trace)
    print("Concept:names:", labels)