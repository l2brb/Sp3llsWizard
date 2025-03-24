import pm4py

# 1. Leggi l'event log (sostituisci il percorso con quello corretto)
event_log = pm4py.read_xes('/home/l2brb/main/DECpietro/evaluation/conformance/real-world/bpic155f/BPIC15_5f.xes')

# 2. Scopri la Petri net utilizzando il metodo Alpha Min


net, initial_marking, final_marking = pm4py.read_pnml("/home/l2brb/main/DECpietro/evaluation/conformance/real-world/bpic155f/BPIC15_5f_alpha.pnml")
fitness = pm4py.conformance.fitness_token_based_replay(
    log=event_log,
    petri_net=net,
    initial_marking=initial_marking,
    final_marking=final_marking,
    activity_key='concept:name',
    timestamp_key='time:timestamp',
    case_id_key='case:concept:name'
)

# 4. Stampa il risultato
print("Fitness:", fitness)