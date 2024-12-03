import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# CSV
df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/d_contraints/results/cleaned_results_rog_dconstraints.csv')

df = df[df['file_name'] % 10 == 0]

# PLOT
plt.style.use("seaborn-v0_8-bright")
plt.figure(figsize=(16,9))

plt.plot(df['file_name'], df['time_ms'], color='purple', linewidth=2, marker='>')

# Beta and R^2
X = df['file_name'].values.reshape(-1, 1)
y = df['time_ms'].values
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
beta = model.coef_[0]
r2 = r2_score(y, y_pred)


print(f"Execution time: Beta = {beta:.4f}, R^2 = {r2:.4f}")


#plt.plot(df['file_name'], y_pred, label='Execution time (Linear fit)', linestyle='--')

plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Increased number of transitions', fontsize=30, labelpad=15)
plt.ylabel('Execution time (ms)', fontsize=30, labelpad=15)
plt.grid(True, linestyle='--')
plt.tight_layout()

plt.xlim([0, 1000])
plt.ylim([0, 60])

plt.legend(['Execution time'], loc='upper left', fontsize=35)

plt.fill_between(df['file_name'], df['time_ms'], color='purple', alpha=0.2)
plt.tight_layout()

plt.savefig('/home/l2brb/main/DECpietro/evaluation/d_contraints/plot/executiontime-trs.pdf')

plt.show()
exit()