import pandas as pd
import matplotlib.pyplot as plt

# Leggi il CSV
df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/results_plctrs.csv')

# PLOT
plt.style.use("seaborn-v0_8-bright")
plt.figure(figsize=(16,9))

# Crea il grafico utilizzando le colonne 'num_transition' e 'mem_usage_mb'
plt.plot(df['num_transition'], df['mem_usage_mb'], color='purple', linewidth=3)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Number of places and transitions', fontsize=30, labelpad=15)
plt.ylabel('Memory usage (MB)', fontsize=30, labelpad=15)
plt.grid(True, linestyle='--')
plt.tight_layout()

plt.xlim([0, df['num_transition'].max()])
plt.ylim([0, df['mem_usage_mb'].max()])

plt.legend(['Memory usage trend'], loc='upper left', fontsize=25)

plt.fill_between(df['num_transition'], df['mem_usage_mb'], color='orchid', alpha=0.1)
plt.tight_layout()
#plt.savefig('/Users/luca/Documents/PythonProjects/TEE_Evaluation/test_memoryusage/memoryusage1.pdf')
plt.savefig('/home/l2brb/main/DECpietro/evaluation/test_place_transition/memoryusage_parallel.pdf')
plt.show()
exit()