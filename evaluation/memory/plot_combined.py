import pandas as pd
import matplotlib.pyplot as plt

# Leggi i CSV
df_trs = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/memory/Dtrs/2_results_transitions_finegrade.csv')
df_places = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/memory/Dtrs/1_results_transitions_finegrade.csv')

# PLOT
plt.style.use("seaborn-v0_8-bright")
plt.figure(figsize=(16,9))

# Crea il grafico utilizzando le colonne 'num_transition' e 'mem_usage_mb' per tutti i dataset
plt.plot(df_trs['num_transition'], df_trs['mem_usage_mb'], color='lightseagreen', linewidth=3, label='Memory usage trend (trs)')
plt.plot(df_places['num_transition'], df_places['mem_usage_mb'], color='salmon', linewidth=3, label='Memory usage trend (places)')

# Imposta i tick dell'asse x in base ai valori della colonna 'num_transition' del dataset con il maggior numero di valori
plt.xticks(sorted(set(df_trs['num_transition']).union(set(df_places['num_transition']))), fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Number of places and transitions', fontsize=30, labelpad=15)
plt.ylabel('Memory usage (MB)', fontsize=30, labelpad=15)
plt.grid(True, linestyle='--')
plt.tight_layout()

# Imposta i limiti degli assi
plt.xlim([0, max(df_trs['num_transition'].max(), df_places['num_transition'].max())])
plt.ylim([0, max(df_trs['mem_usage_mb'].max(), df_places['mem_usage_mb'].max())])

# Aggiungi la legenda
plt.legend(loc='upper left', fontsize=25)

# Aggiungi le aree riempite sotto le curve
plt.fill_between(df_trs['num_transition'], df_trs['mem_usage_mb'], color='lightblue', alpha=0.1)
plt.fill_between(df_places['num_transition'], df_places['mem_usage_mb'], color='salmon', alpha=0.1)

plt.tight_layout()
# Salva il grafico combinato
plt.savefig('/home/l2brb/main/DECpietro/evaluation/test_place_transition/memoryusage_combined.pdf')
plt.show()
exit()