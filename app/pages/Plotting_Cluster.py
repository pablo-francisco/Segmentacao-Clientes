import sys
import os
import streamlit as st

diretorio_atual = os.getcwd()
diretorio_principal = os.path.dirname(diretorio_atual)
sys.path.insert(0, diretorio_principal)

# from src.pipelines import *
# from src.preprocessing import carregar_dados
from app.utils import *
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")


def barplot_site_eda_cluster(df, selected_bar_eda, cluster_col):
    df[selected_bar_eda] = df[selected_bar_eda].astype(str)
    # Agrupar por educação e cluster, contar e calcular a porcentagem
    grouped_df = df.groupby([selected_bar_eda, cluster_col]).size().reset_index(name='Count')
    grouped_df['Percentage'] = round(100 * grouped_df['Count'] / df.shape[0], 1)
    
    fig = go.Figure()

    for education in grouped_df[selected_bar_eda].unique():
        cluster_data = grouped_df[grouped_df[selected_bar_eda] == education]
        x = cluster_data[cluster_col].values
        y = cluster_data['Percentage'].values
        p = [str(k) + '%' for k in y]
        
        fig.add_trace(go.Bar(
            x=x,
            y=y,
            text=p,
            textposition="outside",
            textfont=dict(color="white"),
            orientation="v",
            name=education,
        ))

    layout = go.Layout(
        title=f'Distribuição de {selected_bar_eda} por Clusters',
        xaxis=dict(title='Clusters', tickvals=np.sort(df[cluster_col].unique()), ticktext=np.sort(df[cluster_col].unique())),
        yaxis=dict(title='Distribuição (%)', range=[0, 100]),
        barmode='group'
    )

    fig.update_layout(layout)
    
    return fig

def scatter_site_eda(df,sel_x, sel_y, sel_hue):
    data_filter_eda_bar = df[[sel_x, sel_y, sel_hue]].copy()
    fig = go.Figure(px.scatter(data_frame=data_filter_eda_bar,x=sel_x, y=sel_y, color=sel_hue))
    layout = go.Layout(
        title=f'Gráfico de dispersão entre {sel_x} X {sel_y}',
        xaxis=dict(title=sel_x),
        yaxis=dict(title=sel_y),
    )

    fig.update_layout(layout)
    return fig

def plot_3d_clusters(df,x0,y0,z0):
    hue = 'Clusters'

    df_temp0 = df.copy().sort_values(by=hue)

    x = df_temp0[x0]
    y = df_temp0[y0] 
    z = df_temp0[z0]
    clusters = df_temp0[hue]


    fig = go.Figure()
    for cluster in clusters.unique():

        cluster_data = df_temp0[clusters == cluster]
        fig.add_trace(go.Scatter3d(
            x=cluster_data[x0],
            y=cluster_data[y0],
            z=cluster_data[z0],
            mode='markers',
            marker=dict(
                size=5,
                color= cluster,
                opacity=1,
                colorscale='Viridis'
                
            ),
            name=f'Cluster {cluster}'
        ))


    fig.update_layout(
        title='Visualização de clusters dividos',
        scene=dict(
            xaxis=dict(title=x0),
            yaxis=dict(title=y0),
            zaxis=dict(title=z0),
        )
    )
    return fig

def boxplot_site(df,y):

    fig = px.box(df.sort_values(by='Clusters'), x='Clusters', y=y,points='all',color='Clusters')
    fig.update_layout(
        title='Distribuição dos dados por cluster',
        scene=dict(
            xaxis=dict(title='Clusters'),
            yaxis=dict(title=y),
        
        )
    )
    return fig  




select_categorical = ['Education','Kidhome', 'Teenhome',
                'Recency', 'Complain', 'Response',
                'Promos_Total', 'Age', 'Partner','Has_minor']

select_num = ['Income','MntWines', 'MntFruits', 'MntMeatProducts',
        'MntFishProducts', 'MntSweetProducts', 'MntGoldProds',
        'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases',
        'NumStorePurchases', 'NumWebVisitsMonth', 'Income_per_members', 'Total_spent']

st.markdown("""# Análise de clusters""")

st.markdown("""
            
            
            ## Modelo
            O método para realizar a divisão de clusters foi uma variação do
            K-means, o [K-prototypes](https://pypi.org/project/kmodes/), que
            :green-background[considera as variáveis categóricas em seus cálculos], assim não
            realizando uma clusterização de baixa qualidade considerando todos os valores
            como numéricos, fator que afeta o cálculo de seus centróides.

            ## Redução da dimensionalidade
            Apesar de não ser de necessidade primordial neste projeto, foi utilizada a técnica de
            redução de dimensionalidade [PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html)
            em que extrai apenas os dados principais das features numéricas, :green-background[reduzindo assim a quantidade de dados]
            necessários na etapa de clusterização, assim otimizando o tempo de processamento.

""")

st.markdown('***')

K_new = st.selectbox("Selecione o número de clusters",
                    np.arange(2,11) )

_ , df_out, df_temp3 = relevant_data(K=K_new)

st.markdown('***')


st.markdown("""
            ### Visualização do PCA
            Representação gráfica dos principais componentes utilizados
            para identificar visualmente a qualidade da divisão de dados.""")

col1, col2, col3 = st.columns(3)



# Função para mostrar os clusters em  3D (escolher os PC's)
with col1:
    sel_x = st.selectbox("Eixo X - Selecione um componente", df_temp3.columns.unique()[-9:-1])
with col2:
    sel_y = st.selectbox("Eixo Y - Selecione um componente", df_temp3.columns.unique()[-9:-1] )
with col3:
    sel_z = st.selectbox("Eixo Z - Selecione um componente", df_temp3.columns.unique()[-9:-1] )
st.write(plot_3d_clusters(df_temp3,sel_x,sel_y,sel_z))

st.markdown('***')


st.markdown("""
            ### Distribuição dos clusters
            Representação gráfica dos clusters e em como eles estão distribuídos
            em cada feature analisada, sendo útil para uma :green-background[tomada de decisão
            em conjunto com o time de marketing.]""")

sel_bar = st.selectbox("Selecione a variável", select_categorical )
bar_cat_fig = barplot_site_eda_cluster(df_out, sel_bar, 'Clusters')
st.write(bar_cat_fig)

st.markdown('***')

col1, col2 = st.columns(2)

with col1:
    sel_x = st.selectbox("Eixo X - Selecione uma feature", select_num[::-1])
with col2:
    sel_y = st.selectbox("Eixo Y - Selecione uma feature", select_num )

st.write(scatter_site_eda(df_out.sort_values(by='Clusters'),sel_x,sel_y, 'Clusters'))

st.markdown('***')

sel_y = st.selectbox("Selecione uma feature", select_num )

st.write(boxplot_site(df_out,sel_y))
