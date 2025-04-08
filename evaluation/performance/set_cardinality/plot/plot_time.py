import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score



df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/d_contraints/results/cleaned_results_rog_dconstraints_updated.csv')
df = df[df['file_name'] % 10 == 0]

# PLOT
plt.style.use("seaborn-v0_8-bright")
plt.figure(figsize=(16,9))

column = 'time_ms'

# Regression
X = df['file_name'].values.reshape(-1, 1)
y = df[column].values
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
beta = model.coef_[0]
r2 = r2_score(y, y_pred)

# PLOT
plt.plot(df['file_name'], df[column], label="Execution time [ms]", linewidth=2, color='purple', marker='o')
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('Number of transitions', fontsize=40, labelpad=15)
plt.ylabel('Execution time [ms]', fontsize=40, labelpad=15)
plt.grid(True, linestyle='--')
plt.tight_layout()


legend1 = plt.legend(loc='upper left', fontsize=35, bbox_to_anchor=(0.01, 1))
plt.gca().add_artist(legend1)  
# Box cooridnates
x_pos, y_pos = 0.98, 0.05

legend_text = f"$\\hat{{\\beta}} = {beta:.4f}$, $R_{{\\text{{lin}}}}^2 = {r2:.4f}$"
bbox_props = dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#D3D3D3", linewidth=1)

plt.text(x_pos, y_pos, legend_text, fontsize=35, transform=plt.gca().transAxes,
         verticalalignment='bottom', horizontalalignment='right', bbox=bbox_props)

plt.xlim([0, 1000])
plt.ylim([0, 60])


plt.fill_between(df['file_name'], df['time_ms'], color='purple', alpha=0.2)
plt.subplots_adjust(left=0.09, right=0.967, bottom=0.128, top=0.97)


#plt.savefig('/home/l2brb/main/DECpietro/evaluation/d_contraints/plot/executiontime-trs.pdf')


plt.show()
exit()
