import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from pickle import dump
import math
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

dados = pd.read_csv('Training/CSV/Customers.csv', sep=',')

dados_numericos = dados[['Age', 'AnnualIncome', 'SpendingScore', 'WorkExperience', 'FamilySize']]
dados_categoricos = dados[['Gender', 'Profession']]

# NORMALIZAÇÃO DADOS CATEGÓRICOS
dados_categoricos_normalizados = pd.get_dummies(data=dados_categoricos, prefix_sep='_', dtype=int)
colunas_categoricas = dados_categoricos_normalizados.columns
dump(colunas_categoricas, open("Training/Models/colunas_categoricas.pkl", "wb"))

# NORMALIZAÇÃO DADOS NUMÉRICOS
normalizador = preprocessing.MinMaxScaler()
modelo_normalizador = normalizador.fit(dados_numericos)
dump(modelo_normalizador, open('Training/Models/Normalizer.pkl', 'wb'))

# CRIAR UM DATAFRAME COM OS DADOS NORMALIZADOS
dados_numericos_normalizados = modelo_normalizador.fit_transform(dados_numericos)
dados_numericos_normalizados = pd.DataFrame(data = dados_numericos_normalizados, columns=['Age', 'AnnualIncome', 'SpendingScore', 'WorkExperience', 'FamilySize'])

dados_normalizados_final = dados_numericos_normalizados.join(dados_categoricos_normalizados, how='left')

# DETERMINAR O NUMERO ÓTIMO DE CLUSTERS PELA DISTORÇÃO
distortions = []
K = range(1,100)

for k in K:
    obesidade_kmeans_model = KMeans(n_clusters = k).fit(dados_normalizados_final)
    distortions.append(sum(np.min(cdist(dados_normalizados_final,obesidade_kmeans_model.cluster_centers_,'euclidean'), axis=1) /dados_normalizados_final.shape[0]))

fig, ax = plt.subplots()
ax.plot(K,distortions)
ax.set(xlabel = 'n Clusters', ylabel = 'Distorção', title = 'Elbow pela distorção')
ax.grid()
fig.savefig('Training/elbow_distorcao.png')
plt.show()

x0 = K[0]
y0 = distortions[0]
xn = K[len(K) -1]
yn = distortions[len(distortions)-1]

distancias = []
for i in range(len(distortions)):
    x = K[i]
    y = distortions[i]
    numerador = abs((yn-y0) * x - (xn-x0) * y + xn * y0 - yn * x0)
    denominador = math.sqrt((yn-y0)**2 + (xn - x0)**2)
    distancias.append(numerador/denominador)
n_clusters_otimos = K[distancias.index(np.max(distancias))]

# TREINAR O MODELO DEFINITIVO
obesidade_kmeans_model = KMeans(n_clusters = n_clusters_otimos, random_state=42).fit(dados_normalizados_final)
dump(obesidade_kmeans_model, open('Training/Models/shop_customers_clusters_2024.pkl', 'wb'))