import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/realworld/results/results_log_literature.csv')

# PLOT
plt.style.use("ggplot")
plt.figure(figsize=(16,9))
colors = plt.cm.viridis(np.linspace(0, 1, len(df['file_name'])))

plt.bar(df['file_name'], df['mem_usage_mb'], color=colors, linewidth=2)
plt.xticks(fontsize=15, rotation=45)
plt.yticks(fontsize=20)
plt.xlabel('Real-world process models', fontsize=30, labelpad=15)
plt.ylabel('Memory usage (MB)', fontsize=30, labelpad=15)
plt.tight_layout()

plt.xlim([-0.5, df['file_name'].max()])
plt.ylim([0, 25])

#plt.legend(['Execution time'], loc='upper left', fontsize=25)

plt.tight_layout()
#plt.savefig('/home/l2brb/main/DECpietro/evaluation/memory/plot/real-memory.pdf')
plt.show()