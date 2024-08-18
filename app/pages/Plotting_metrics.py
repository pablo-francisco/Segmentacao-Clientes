import sys
import os
import streamlit as st

diretorio_atual = os.getcwd()
# diretorio_principal = os.path.dirname(diretorio_atual)
sys.path.insert(0, diretorio_atual)

from app.utils import *
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")


def create_individual_line_charts(df_temp):
    figures = []
    for column in df_temp.columns[:-1]:
        fig = go.Figure()

        # Adicionando o trace para a coluna atual
        fig.add_trace(go.Scatter(
            x=df_temp['N° Cluster'],
            y=df_temp[column],
            mode='lines+markers',
            name=column
        ))

        # Atualizando o layout do gráfico
        fig.update_layout(
            title=f'Gráfico de Linha - {column}',
            xaxis_title='N° Cluster',
            yaxis_title=column,
            template='plotly_dark'
        )

        # Mostrando o gráfico
        figures.append(fig)
    return figures

df_metrics = pd.read_csv(f'{diretorio_atual}/data/metrics/Clusters_scores.csv').iloc[:,1:]

f_1,f_2,f_3 = create_individual_line_charts(df_metrics)

on = st.toggle("Mostrar equações")


st.markdown('# Métricas de avaliação do cluster')

st.markdown("""
Na análise de clusters, é fundamental utilizar métricas para :blue-background[avaliar a qualidade dos agrupamentos].
 Três das métricas mais comuns são o **Silhouette Score**, o **Calinski-Harabasz Index** e
 o **Davies-Bouldin Index**.

""")
 
st.markdown("""
            É realizada uma análise para esses índices em um alcance
            variando de :blue-background[2 à 10 clusters] e depois apresentados seus resultados
            a seguir.

""")


st.write('## Shillouette Score')

st.markdown(""" 
    
            O [Silhouette Score](https://medium.com/@haataa/how-to-measure-clustering-performances-when-there-are-no-ground-truth-db027e9a871c)
             mede o quão similar cada ponto de um 
            cluster é em relação aos pontos do próprio cluster (coesão) comparado
             com os pontos de outros clusters (separação).


            O valor do Silhouette Score varia de -1 a 1:
            - Valores próximos a 1 indicam clusters bem definidos.
            - Valores próximos a 0 indicam clusters sobrepostos.
            - Valores negativos indicam que os pontos podem estar em clusters errados.

""")

if on:
    st.latex(r"""s(i) = \frac{b(i) - a(i)}{max\{ a(i), b(i) \}}""")

st.write(f_1)

st.markdown('***')

st.write('## Calinski-Harabasz Index')

st.markdown("""
O [Calinski-Harabasz Index](https://medium.com/@haataa/how-to-measure-clustering-performances-when-there-are-no-ground-truth-db027e9a871c)
             (ou **Variance Ratio Criterion**) mede a densidade dos clusters.
Ele é definido como a razão entre a soma da dispersão entre clusters e a soma da dispersão dentro dos clusters.
            
Valores mais altos do Calinski-Harabasz Index indicam uma melhor definição dos clusters.

            """)
if on:
    st.latex(r"""CH = \frac{ \text{tr}(B_k) }{ \text{tr}(W_k) } \times \frac{N - k}{k - 1}""")

st.write(f_2)

st.write('## Davies-Bouldin Index')

st.markdown("""
            O [Davies-Bouldin Index](https://medium.com/@haataa/how-to-measure-clustering-performances-when-there-are-no-ground-truth-db027e9a871c)
            mede a média das razões entre
            a soma das dispersões dentro dos clusters e a separação entre os clusters.

            Valores mais baixos do Davies-Bouldin Index indicam clusters melhor definidos.
            """)
if on:
    st.latex(r""" DB = \frac{1}{k} \sum_{i=1}^{k} \max_{j \neq i} \left( \frac{\sigma_i + \sigma_j}{d(c_i, c_j)} \right)""")

st.write(f_3)

st.markdown("""
            ## Conclusões
            Devido ao comportamento dos gráficos, :blue-background[o número de clusters ideais é de
            K = 2], porém essa divisão :red-background[não segmenta os dados em uma quantidade relevante] para aplicações
            reais.

            O ideal seria a coleta de uma quantidade maior de dados e realizar o mesmo procedimento na tentativa de encontrar
            índices melhores, ou seja, que permitam uma maior flexibilidade no número de clusters.
            """)