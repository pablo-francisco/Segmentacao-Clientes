import sys
import os
import streamlit as st

diretorio_atual = os.getcwd()

sys.path.insert(0, diretorio_atual)

from app.utils import *
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")



def barplot_site_eda(df, selected_bar_eda):
    data_filter_eda_bar = round(100*df[selected_bar_eda].value_counts() / df.shape[0], 1)
    
    x = data_filter_eda_bar.index.values
    y = data_filter_eda_bar.values
    p = [str(k) + '%' for k in data_filter_eda_bar.values]

    fig = go.Figure(
            go.Bar(
                x=x,
                y=y,
                text=p,
                textposition="outside",
                textfont=dict(color="white"),
                orientation="v",
                marker_color=['#45056e', '#e85d04', '#7a057e', '#ff8200', '#a64ed1', '#ff9c33'],
                
            )
    )

    layout = go.Layout(
        title=f'Distribuição de {selected_bar_eda}',
        xaxis=dict(title=selected_bar_eda,tickvals=x,ticktext=x),
        yaxis=dict(title='Distribuição (%)',range=[0, np.min([max(y)*1.15,115])]),
    ) 

    fig.update_layout(layout)

    return fig

def scatter_site_eda(df,sel_x, sel_y, sel_hue):
    data_filter_eda_bar = df[[sel_x, sel_y, sel_hue]].copy()
    data_filter_eda_bar[sel_hue] = data_filter_eda_bar[sel_hue].astype(str)

    fig = go.Figure(px.scatter(data_frame=data_filter_eda_bar,x=sel_x, y=sel_y, color=sel_hue))
    layout = go.Layout(
        title=f'Gráfico de dispersão entre {sel_x} X {sel_y}',
        xaxis=dict(title=sel_x),
        yaxis=dict(title=sel_y),
    )

    fig.update_layout(layout)
    return fig

select_categorical = ['Education','Kidhome', 'Teenhome',
                'Recency', 'Complain', 'Response',
                'Promos_Total', 'Age', 'Partner','Has_minor']

select_num = ['Income','MntWines', 'MntFruits', 'MntMeatProducts',
        'MntFishProducts', 'MntSweetProducts', 'MntGoldProds',
        'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases',
        'NumStorePurchases', 'NumWebVisitsMonth', 'Income_per_members', 'Total_spent']


st.markdown('# Análise de dados')

df_temp1, _ , _ = relevant_data(K = 2)


st.markdown("""

            Realizar uma :blue-background[análise exploratória de dados (EDA)] é uma etapa
            essencial que sustenta todo o processo de ciência de dados.
            A EDA não só melhora a compreensão dos dados, mas também garante que as análises subsequentes sejam baseadas em informações sólidas e confiáveis.
            
            Essa prática é indispensável para alcançar insights valiosos e tomar decisões informadas que impulsionam o sucesso organizacional.

            Algumas das justificativas de utilizar EDA:

            * Compreender estrutura e distribuição dos dados
            * Análise de qualidade dos dados, detectando outliers e valores faltantes
            * Detecção de padrões e relações entre os dados

""")

st.markdown('***')

## barplot (escolher categorias)

st.markdown('## Distribuição de dados categóricos')

selected_bar_eda = st.selectbox("Selecione a categoria",
                                    select_categorical )

st.write(barplot_site_eda(df_temp1, selected_bar_eda))

st.markdown("""
1. O nível de escolaridade da :blue-background[maioria dos clientes] é a graduação, seguido por pós-graduados e com uma parcela inferior os não graduados.

2. O período **desde a última compra dos clientes** está bem distribuido entre os períodos de **menores que 1 mês, entre 1-2 e entre 2-3 meses**,
             com menores proporções (8.8%) de ocorrências em intervalos de compra **maiores que 3 meses**.


3. As idades de cadastro na empresa como cliente são mais mais frequentes no grupo de pessoas com de :blue-background[meia-idade] em relação as outras faixas etárias adotadas.

4. Percebe-se que há divisão ao limiar do balanço entre a classe "Partner", onde **52.9% dos consumidores não possuem parceiros em relacionamentos**.
5. Uma :red-background[taxa de reclamações] vinda dos consumidores é baixa em relação ao total de clientes, em que apenas **0.9%** abriram pedidos de reclamação.
6. Os proporção entre consumidores que aceitaram pelo menos uma das propostas de desconto, indica que :red-background[mais de 2/3 dos clientes não aceitaram nenhuma das ofertas],
             seguido por :green-background[14.6% aceitarem em pelo menos uma das 5 ofertas] oferecidas, e os demais totalizando cerca de **6.2%** dos clientes **aceitaram mais de uma oferta**.
7. Cerca de **15%** dos clientes :green-background[aceitaram a última oferta] realizada à eles.

8. A proporção de pessoas com **pelo menos um menor de idade** é de **71.4%** em relação ao conjunto de dados total.
9. A quantidade de clientes que possuem **mais de 2** adolescentes ou crianças é baixa, **2.3% e 2.1% respectivamente**.
""")

st.markdown('***')
#scatter
st.markdown('## Distribuição de dados numéricos')
col1, col2,col3 = st.columns(3)


with col1:
    sel_x = st.selectbox("Eixo X - Selecione uma feature", select_num )
with col2:
    sel_y = st.selectbox("Eixo Y - Selecione uma feature", select_num[::-1] )
with col3:
    sel_hue = st.selectbox("Selecione a feature a ser destacada", select_categorical )
st.write(scatter_site_eda(df_temp1,sel_x, sel_y, sel_hue))

st.markdown("""

        1. Pessoas com renda acima de aproximadamente 50K
             :green-background[aumentam seu poder de compra] em todos os produtos.
        2. Clientes com renda abaixo de aproximadamente 50K aceitaram a apenas uma promoção.
        
        
        
""")