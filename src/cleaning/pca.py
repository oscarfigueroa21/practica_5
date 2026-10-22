import pandas as pd
from sklearn.decomposition import PCA

FECHA_CORTE = '2009-12-31 23:59:00'

def dimensionalidad(df_limpio):
    df_limpio = df_limpio.drop(columns='Global_intensity')
    return df_limpio

def aplicar_pca(df_limpio, fecha_corte=FECHA_CORTE, varianza_objetivo=0.8):
    pca = PCA(n_components=varianza_objetivo)
    pca.fit(df_limpio.loc[:fecha_corte])

    datos_pca = pca.transform(df_limpio)
    columnas_pca = [f'Componente_{i+1}' for i in range(pca.n_components_)]
    df_pca = pd.DataFrame(datos_pca, columns=columnas_pca, index=df_limpio.index)
    return df_pca, pca

def obtener_loadings(pca, columnas_originales):
    pesos = pca.components_
    nombres_filas = [f'PC{i+1}' for i in range(pca.n_components_)]
    df_pesos = pd.DataFrame(pesos, columns=columnas_originales, index=nombres_filas)
    return df_pesos

def incorporar_pca(df_limpio, df_pca):
    return df_limpio.join(df_pca)
