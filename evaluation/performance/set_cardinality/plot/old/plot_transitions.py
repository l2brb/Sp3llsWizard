import pandas as pd
import matplotlib.pyplot as plt

# CSV
df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/d_contraints/results/cleaned_results_rog_dconstraints.csv')

df = df[df['file_name'] % 40 == 0]

# PLOT
plt.style.use("seaborn-v0_8-bright")
plt.figure(figsize=(16,9))

plt.plot(df['file_name'], df['mem_usage_mb'], color='purple', linewidth=2, marker='>')
# plt.plot(df['file_name'], df['avg_mem_overall_mb'], color='purple', linewidth=2, marker='o')
# plt.plot(df['file_name'], df['peak_mem_mb'], color='purple', linewidth=2, marker='o')

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Number of transformation iterations', fontsize=30, labelpad=15)
plt.ylabel('Memory usage (MB)', fontsize=30, labelpad=15)
#plt.xscale('log')  # Set x-axis to logarithmic scale
plt.grid(True, linestyle='--')
plt.tight_layout()

# plt.xlim([0, df['file_name'].max()])  # Set lower limit to 1 for log scale
plt.ylim([0, 50])
plt.xlim([0, 1000]) 

plt.legend(['Memory usage'], loc='upper left', fontsize=25)

plt.fill_between(df['file_name'], df['mem_usage_mb'], color='purple', alpha=0.1)
plt.tight_layout()
#plt.savefig('/Users/luca/Documents/PythonProjects/TEE_Evaluation/test_memoryusage/memoryusage1.pdf')
#plt.savefig('/home/l2brb/main/DECpietro/evaluation/memory/plot/executiontime-trs.pdf')
plt.show()
exit()