import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures

# Leggi il CSV
df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/n_constraints/results/cleaned/cleaned_results_rog_complete_extra_5k_update.csv')

# Filtra il DataFrame per includere solo i file_name che sono multipli di 10
df = df[df['file_name'] % 40 == 0]

# PLOT
plt.style.use("seaborn-v0_8-bright")
plt.figure(figsize=(16,9))

# Crea il grafico utilizzando le colonne 'file_name' e le altre colonne di interesse
columns_of_interest = [
    'mem_usage_mb'
]

for column in columns_of_interest:
    plt.plot(df['file_name'], df[column], label=column, linewidth=2, color= 'lightseagreen', marker='o')

    # Calcola la pendenza Beta e la bontà di adattamento R^2
    X = df['file_name'].values.reshape(-1, 1)
    y = df[column].values
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    beta = model.coef_[0]
    r2 = r2_score(y, y_pred)

    # Stampa i risultati
    print(f"{column}: Beta = {beta:.4f}, R^2 = {r2:.4f}")


#plt.plot(df['file_name'], y_pred, label=f'{column} (Linear fit)', linestyle='--', color='darkseagreen', alpha=0.7)

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Number of transformation iterations', fontsize=30, labelpad=15)
plt.ylabel('Memory usage (MB)', fontsize=30, labelpad=15)
plt.grid(True, linestyle='--')
plt.tight_layout()

plt.legend(['Memory usage'], loc='upper left', fontsize=35)


plt.xlim([0, 1000])
plt.ylim([0, 100])


plt.fill_between(df['file_name'], df['mem_usage_mb'], color='lightseagreen', alpha=0.2)
# plt.fill_between(df['file_name'], df['peak_mem_mb'], color='red', alpha=0.2)
# plt.fill_between(df['file_name'], df['avg_mem_overall_mb'], color='green', alpha=0.2)
# plt.fill_between(df['file_name'], df['peak_mem_petri_parser_mb'], color='purple', alpha=0.2)
# plt.fill_between(df['file_name'], df['avg_mem_dec_translator_mb'], color='orange', alpha=0.2)
# plt.fill_between(df['file_name'], df['peak_mem_dec_translator_mb'], color='brown', alpha=0.2)


plt.savefig('/home/l2brb/main/DECpietro/evaluation/n_constraints/plot/pdf/memoryusage.pdf')

plt.show()
exit()