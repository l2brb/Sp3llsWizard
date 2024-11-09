import pandas as pd
import matplotlib.pyplot as plt

# CSV
df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/time/Dplace/1_results_places_finegrade.csv')
# PLOT
plt.style.use("seaborn-v0_8-bright")
plt.figure(figsize=(16,9))


plt.plot(df['num_transition'], df['time_ms'], color='purple', linewidth=3, marker='>', markersize=12)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Number of  places (stable transitions)', fontsize=30, labelpad=15)
plt.ylabel('Execution TIme (ms)', fontsize=30, labelpad=15)
plt.grid(True, linestyle='--')
plt.tight_layout()

plt.xlim([0, df['num_transition'].max()])
plt.ylim([0, df['time_ms'].max()])

plt.legend(['Execution time trend'], loc='upper left', fontsize=25)

plt.fill_between(df['num_transition'], df['time_ms'], color='purple', alpha=0.1)
plt.tight_layout()
#plt.savefig('/Users/luca/Documents/PythonProjects/TEE_Evaluation/test_memoryusage/memoryusage1.pdf')
plt.savefig('/home/l2brb/main/DECpietro/evaluation/test_place_transition/time/time-place.pdf')
plt.show()
exit()
