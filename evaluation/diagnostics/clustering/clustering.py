import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import KMeans
import seaborn as sns


# Leggi il CSV
df = pd.read_csv('/home/l2brb/main/DECpietro/evaluation/conformance/clustering/bpic15.csv', header=0, delimiter='\t')
#print(df.head())

df = df[df.iloc[:, 10] != 1]
trace_fitness = df.iloc[:, 10].values.reshape(-1, 1)
#print(trace_fitness)
#print(trace_fitness)


############################ Hierarchical Clustering
Z = linkage(trace_fitness, method='ward')

# plt.figure(figsize=(10, 4))
# plt.title("Dendrogram for Hierarchical Clustering")
# plt.xlabel("Index")
# plt.ylabel("Distance")
# dendrogram(Z)
#plt.show()

clusters = fcluster(Z, t=4, criterion='maxclust')
df['Cluster'] = clusters

plt.figure(figsize=(10, 7))
plt.scatter(df.index, df.iloc[:, 10], c=df['Cluster'], cmap='viridis')
plt.title("Scatter Plot of Trace Fitness Clusters")
plt.xlabel("Index")
plt.ylabel("Trace Fitness")
plt.colorbar(label='Cluster')
#plt.show()
#print(df.iloc[:, [0, 10, 15]])
#print(df.head())



###############################  SUBFRAME

df_subset = df.iloc[:, [0, 10, 15]]
df_subset.columns = ['Constraint', 'Fitness', 'Cluster']
#print(df_subset.head())
#df_subset = df_subset[df_subset['Fitness'] != 1]


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(df_subset)


mean_fitness = df_subset.groupby('Cluster')['Fitness'].mean()
#print(mean_fitness)



#Boxplot + Swarmplot
"""plt.figure(figsize=(12, 8))
sns.boxplot(x='Cluster', y='Fitness', data=df_subset, palette='viridis')
sns.swarmplot(x='Cluster', y='Fitness', data=df_subset, color='black', alpha=0.7)
plt.title("Distribution of Fitness Values per Cluster")
plt.xlabel("Cluster")
plt.ylabel("Fitness")
plt.tight_layout()
plt.show()"""

pivot_table = df_subset.pivot_table(index='Constraint', columns='Cluster', values='Fitness', aggfunc='mean')

# Visualizza la heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(pivot_table, annot=True, fmt=".3f", cmap='viridis')
plt.title("Heatmap of Mean Fitness per Constraint by Cluster")
plt.xlabel("Cluster")
plt.ylabel("Constraint")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

exit()










"""
#KMEANS
kmeans = KMeans(n_clusters=4, random_state=0).fit(trace_fitness)
kmeans_clusters = kmeans.labels_
print("KMeans Cluster assignments:", kmeans_clusters)
df['KMeans Cluster'] = kmeans_clusters

# Scatter plot per i cluster KMeans
plt.figure(figsize=(10, 7))
plt.scatter(df.index, df.iloc[:, 10], c=df['KMeans Cluster'], cmap='viridis')
plt.title("Scatter Plot of Trace Fitness - KMeans Clustering")
plt.xlabel("Index")
plt.ylabel("Trace Fitness")
plt.colorbar(label='KMeans Cluster')
plt.show()"""