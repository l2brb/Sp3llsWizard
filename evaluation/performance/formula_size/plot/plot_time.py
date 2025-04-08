import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# Leggi il CSV
df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/n_constraints/results/results_rog_nconstraints_updated_bugfix.csv')

# Filtra il DataFrame per includere solo i file_name che sono multipli di 20
df = df[df['file_name'] % 10 == 0]

# PLOT
plt.style.use("seaborn-v0_8-bright")
plt.figure(figsize=(16,9))

# Crea il grafico utilizzando le colonne 'file_name' e 'time_ms'
plt.plot(df['file_name'], df['time_ms'], color='lightseagreen', linewidth=2, marker='o')

# Calcola la pendenza Beta e la bontà di adattamento R^2
X = df['file_name'].values.reshape(-1, 1)
y = df['time_ms'].values
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
beta = model.coef_[0]
r2 = r2_score(y, y_pred)


#print(f"Execution time: Beta = {beta:.4f}, R^2 = {r2:.4f}")

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Number of transformation iterations', fontsize=40, labelpad=15)
plt.ylabel('Execution time [ms]', fontsize=40, labelpad=15)
plt.grid(True, linestyle='--')

# **Box Metrics**
x_pos, y_pos = 0.98, 0.05  # Posizionato in basso a destra (come il grafico della memoria)
legend_text = f"$\\hat{{\\beta}} = {beta:.4f}$, $R_{{\\text{{lin}}}}^2 = {r2:.4f}$"
bbox_props = dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#D3D3D3", linewidth=1)

# Inserisce il testo dentro il box con perfetto allineamento
plt.text(x_pos, y_pos, legend_text, fontsize=35, transform=plt.gca().transAxes,
         verticalalignment='bottom', horizontalalignment='right', bbox=bbox_props)

plt.xlim([0, 1000])
plt.ylim([0, 600])


plt.legend(['Execution time [ms]'], loc='upper left', fontsize=35)


plt.fill_between(df['file_name'], df['time_ms'], color='lightseagreen', alpha=0.2)


plt.subplots_adjust(left=0.105, right=0.967, bottom=0.135, top=0.97)


plt.savefig('/home/l2brb/main/DECpietro/evaluation/n_constraints/plot/pdf/executiontime.pdf')

#plt.show()
exit()
