import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


# Leggi il CSV
df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/d_contraints/results/cleaned_results_rog_dconstraints_updated_bugfix.csv')

# Filtra il DataFrame per includere solo i file_name che sono multipli di 40
df = df[df['file_name'] % 40 == 0]

# PLOT
plt.style.use("seaborn-v0_8-bright")
plt.figure(figsize=(16,9))

# Colonne di interesse
column = 'mem_usage_mb'

# Regression
X = df['file_name'].values.reshape(-1, 1)
y = df[column].values
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
beta = model.coef_[0]
r2 = r2_score(y, y_pred)

# PLOT
plt.plot(df['file_name'], df[column], label="Memory Usage [MB]", linewidth=2, color='purple', marker='o')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Number of transitions', fontsize=40, labelpad=15)
plt.ylabel('Memory usage [MB]', fontsize=40, labelpad=15)
plt.grid(True, linestyle='--')
plt.tight_layout()


# Prima legenda Memory Usage
legend1 = plt.legend(loc='upper left', fontsize=35, bbox_to_anchor=(0.01, 1))
plt.gca().add_artist(legend1)  



# Box cooridnates
x_pos, y_pos = 0.98, 0.05

legend_text = f"$\\hat{{\\beta}} = {beta:.4f}$, $R_{{\\text{{lin}}}}^2 = {r2:.4f}$"
bbox_props = dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#D3D3D3", linewidth=1)

# Inserisce il testo dentro il box con perfetto allineamento
plt.text(x_pos, y_pos, legend_text, fontsize=35, transform=plt.gca().transAxes,
         verticalalignment='bottom', horizontalalignment='right', bbox=bbox_props)



plt.xlim([0, 1000]) 
plt.ylim([0, 50])


plt.fill_between(df['file_name'], df['mem_usage_mb'], color='purple', alpha=0.2)



plt.subplots_adjust(left=0.09, right=0.967, bottom=0.127, top=0.97)


plt.savefig('/home/l2brb/main/DECpietro/evaluation/d_contraints/plot/memoryusage-trs.pdf')


plt.show()
exit()
