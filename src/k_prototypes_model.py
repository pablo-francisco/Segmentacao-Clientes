import numpy as np
from kmodes.kprototypes import KPrototypes
import streamlit as st

def clusterizar_dados_kprototypes(df_temp,k,
                                  cat_columns,gamma=None):
    """
    Realiza a operação de clusterização.

    Input:
    df_temp -- Dataframe utilizado
    k -- N° de clusters
    cat_columns -- Colunas categóricas
    gamma -- Balanço entre dados categóricos e numéricos no modelo.


    Output:
    clusters -- Clusters para cada ponto analisado
    kproto -- modelo de clusterização
    """
    cat_index = list(np.arange(0,len(cat_columns)))
    kproto = KPrototypes(n_clusters=k, init='Cao', n_init=10, verbose=0,random_state=42,gamma=gamma)
    clusters = kproto.fit_predict(df_temp, categorical=cat_index)
    return clusters,kproto

def fit_pred_data(df_original,df_temp,K,cat_relevant):
    """
    Mescla os dados originais com os clusters previstos.

    Input:
    df_temp -- Dataframe utilizado
    k -- N° de clusters
    cat_columns -- Colunas categóricas
    gamma -- Balanço entre dados categóricos e numéricos no modelo.


    Output:
    df_final -- Dataframe clusterizado
    kproto -- modelo de clusterização
    """

    df_final = df_original.copy()
    clusters_divididos, kproto = clusterizar_dados_kprototypes(df_temp,K,cat_relevant)
    df_final['Clusters'] = clusters_divididos
    return df_final, kproto

