import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os



directory = '/home/l2brb/main/DECpietro/evaluation/conformance/clustering/output_minerful'






data = []
constraint_names = None

# Leggi tutti i file CSV nella directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath, header=0, delimiter=';')
        
        # Estrai i valori di fitness dei constraint
        fitness_values = df.iloc[:, 10].values
        data.append(fitness_values)
        
        # Estrai i nomi dei constraint dalla prima colonna
        if constraint_names is None:
            constraint_names = df.iloc[:, 0].values

# Converti i dati in un DataFrame
data = np.array(data).T  # Trasponi per avere i sublog sulle colonne
sublogs = [filename for filename in os.listdir(directory) if filename.endswith('.csv')]

df_heatmap = pd.DataFrame(data, index=constraint_names, columns=sublogs)

# Crea la heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(df_heatmap, cmap='viridis', annot=True, fmt=".2f")
plt.title("Heatmap of Trace Fitness Across Sublogs")
plt.xlabel("Sublog")
plt.ylabel("Constraint")
plt.xticks(rotation=90)  # Ruota le etichette dell'asse x per una migliore leggibilità
plt.tight_layout()  # Adatta il layout per evitare sovrapposizioni
plt.show()























exit()
means = []
sublogs = [] 

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath, header=0, delimiter=';')


        mean_value = df.iloc[:, 10].mean()
        means.append(mean_value)
        sublogs.append(filename)  #

plt.figure(figsize=(10, 7))
plt.plot(sublogs, means, marker='o', linestyle='-', color='b')
plt.title("Mean of Trace Fitness Across Sublogs")
plt.xlabel("Sublog")
plt.ylabel("Mean Trace Fitness")
plt.xticks(rotation=90)  # Ruota le etichette dell'asse x per una migliore leggibilità
plt.grid(True)
plt.tight_layout()  # Adatta il layout per evitare sovrapposizioni
plt.show()