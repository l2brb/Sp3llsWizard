import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Leggi il CSV
df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/n_constraints/results/cleaned/cleaned_results_rog_complete_extra_5k_update.csv')


# Filtra il DataFrame per includere solo i file_name che sono multipli di 40
df = df[df['file_name'] % 20 == 0]

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

# Stampa i risultati
print(f"Execution time: Beta = {beta:.4f}, R^2 = {r2:.4f}")

# Disegna la retta di regressione lineare
#plt.plot(df['file_name'], y_pred, label='Execution time (Linear fit)', linestyle='--')

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Number of transformation iterations', fontsize=30, labelpad=15)
plt.ylabel('Execution time (ms)', fontsize=30, labelpad=15)
plt.grid(True, linestyle='--')
plt.tight_layout()

plt.xlim([0, 1000])
plt.ylim([0, 500])

plt.legend(['Execution time'], loc='upper left', fontsize=35)

plt.fill_between(df['file_name'], df['time_ms'], color='lightseagreen', alpha=0.2)
plt.tight_layout()

plt.savefig('/home/l2brb/main/DECpietro/evaluation/n_constraints/plot/pdf/executiontime.pdf')

plt.show()
exit()