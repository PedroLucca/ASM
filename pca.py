from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt

#Teste de entradas
df = pd.DataFrame({
    'var1': [1,3,1,2,2,1],
    'var2': [2,4,3,4,3,4],
    'target': [0,1,0,1,1,1]
})

x = df.drop('target', 1)
y = df['target']

pca = PCA(n_components = 2)
pca.fit(x)

print(pca.components_)