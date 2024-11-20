import pandas as pd
import matplotlib.pyplot as plt

# Leggi il CSV
df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/memory/cleaned_results_rog_t1-2a.csv')

# Filtra il DataFrame per includere solo i file_name che sono multipli di 50
df = df[df['file_name'] % 10 == 0]

# PLOT
plt.style.use("seaborn-v0_8-bright")
plt.figure(figsize=(16,9))

# Crea il grafico utilizzando le colonne 'file_name' e 'time_ms'
plt.plot(df['file_name'], df['time_ms'], color='lightseagreen', linewidth=2)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Number of transformation iterations', fontsize=30, labelpad=15)
plt.ylabel('Execution time (ms)', fontsize=30, labelpad=15)
#plt.xscale('log')  # Set x-axis to logarithmic scale
plt.grid(True, linestyle='--')
plt.tight_layout()

plt.xlim([1, df['file_name'].max()])  # Set lower limit to 1 for log scale
plt.ylim([0, df['time_ms'].max()])

plt.legend(['Execution time'], loc='upper left', fontsize=25)

plt.fill_between(df['file_name'], df['time_ms'], color='lightseagreen', alpha=0.2)
plt.tight_layout()
#plt.savefig('/Users/luca/Documents/PythonProjects/TEE_Evaluation/test_memoryusage/memoryusage1.pdf')
plt.savefig('/home/l2brb/main/DECpietro/evaluation/memory/plot/executiontime-trs.pdf')
plt.show()
exit()