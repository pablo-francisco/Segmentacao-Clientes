import sys
import os
import streamlit as st
from scipy import stats

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

diretorio_atual = os.getcwd()
diretorio_principal = os.path.dirname(diretorio_atual)
sys.path.insert(0, diretorio_principal)


def calcular_correlacao(df_temp,columns,selec_column):
    v_temp = df_temp[columns].corr()[selec_column]
    return pd.DataFrame(v_temp.sort_values())

# Função para calcular a cor baseada na correlação, se aproximando do branco
def calculate_color(correlation):
    if correlation < 0:
        red = int(255 * (1 - abs(correlation)))
        return f'rgb(255, {red}, {red})'
    else:
        blue = int(255 * (1 - correlation))
        return f'rgb({blue}, {blue}, 255)'

def site_plot_corr(correlated_values):

    # Definindo as cores: vermelho para correlações negativas e azul para positivas
    colors = [calculate_color(val) for val in correlated_values.values]

    fig = go.Figure(go.Bar(
        x=correlated_values.index,
        y=correlated_values.values.flatten(),
        marker_color=colors
    ))

    fig.update_layout(
        title=f'Correlação das Variáveis com {correlated_values.columns[0]}',
        xaxis_title='',
        yaxis_title='Correlação',
        yaxis=dict(range=[-1, 1])
    )

    return fig


def site_calculate_chi2(df_temp,sel_1,sel_2):
    
    # Tabela de contingência entre Education e Response
    contingency_table = pd.crosstab(df_temp[sel_1], df_temp[sel_2])

    # Aplicando o teste Qui-Quadrado
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table,
                                                    correction=False)
    sufficient_samples = all(expected.flatten() > 5)


    relatory_chi = pd.DataFrame()
    relatory_chi['Chi2'] = [chi2]
    relatory_chi['P-value'] = [p]
    relatory_chi['Degrees of freedom'] = [dof]
    relatory_chi['Associação significativa (p <= 0.05)'] = ['Sim' if p <0.05 else 'Não']
    relatory_chi['Amostras Suficientes (todas esperadas > 5)'] = ['Sim' if sufficient_samples else 'Não']

    return contingency_table, relatory_chi


def site_plot_chi(contingency_table):

    fig = go.Figure()

    for column in contingency_table.columns:
        fig.add_trace(go.Bar(
            x=contingency_table.index,
            y=contingency_table[column],
            name=f"{column}",
            text=contingency_table[column],
            textposition='outside'

        ))
    # Layout do gráfico
    fig.update_layout(
        title=f"Contagem de Amostras associado ao P-Value",
        xaxis_title=f"{contingency_table.index.name}",
        yaxis_title="Quantidade de Amostras",
        barmode='group',
        legend_title=f"{contingency_table.columns.name}" 
    )
        
    return fig

def site_calculate_anova(df_temp,
                         cat_col,
                         num_cols):
    
    df_temp1 = pd.DataFrame()

    for num_col in num_cols:
    
        groups = [df_temp[num_col][df_temp[cat_col] == category] for category in df_temp[cat_col].unique()]
        anova_result = stats.f_oneway(*groups)
        df_report = pd.DataFrame(anova_result,
                    index=['F-statistic','p-value'],
                    columns = [f'{num_col}']).T
        
        df_report['Associado'] = ['Sim' if anova_result.pvalue < 0.05 else 'Não']
        
        df_temp1 = pd.concat([df_temp1,df_report],axis=0)

    return df_temp1.sort_values(by='p-value',ascending=False)

def highlight_row(row):
    return ['background-color: green' if row['Associado'] == 'Sim' else 'background-color: red' for _ in row]


path_preprocessed = f'data\\processed\\marketing_campaign_processed.csv'

df_preprocessed = pd.read_csv(path_preprocessed)

cat_stat_columns = ['Education','Kidhome',
                    'Teenhome','Recency','Complain',
                    'Response','Promos_Total','Age','Partner']

num_stat_columns = ['Income','MntWines','MntFruits','MntMeatProducts',
                    'MntFishProducts','MntSweetProducts','MntGoldProds',
                    'NumDealsPurchases','NumWebPurchases',
                    'NumCatalogPurchases','NumStorePurchases',
                    'NumWebVisitsMonth','Income_per_members',
                    'Total_spent']

on = st.toggle("Mostrar equações")


st.markdown(""" 
# A Importância da Análise Estatística

A análise estatística é uma ferramenta fundamental para :green-background[transformar dados em informações úteis e relevantes]. Ela permite identificar padrões, 
tendências e relações entre variáveis, ajudando na tomada de decisões informadas. No mundo dos negócios, por exemplo, a análise estatística pode 
revelar insights sobre o comportamento dos clientes, prever demandas futuras e otimizar estratégias de marketing. Além disso, a estatística 
fornece os métodos necessários para validar hipóteses e testar a significância dos resultados, garantindo que as :green-background[conclusões tiradas dos dados 
sejam confiáveis] e não fruto do acaso.
""")


st.markdown(""" 
            ## Correlação de pearson
            
            A Correlação é uma medida estatística que indica o :blue-background[grau de relação entre duas variáveis numéricas]. Se duas variáveis possuem uma correlação alta, isso 
            significa que à medida que uma varia, a outra tende a variar de maneira previsível. A correlação pode ser positiva (ambas as variáveis aumentam 
            ou diminuem juntas) ou negativa (uma variável aumenta enquanto a outra diminui).

""")


if on:
    st.latex(r"""r = \frac{\sum (x_i - \overline{x})(y_i -
            \overline{y})}{\sqrt{\sum (x_i - \overline{x})^2 \sum(y_i - \overline{y})^2}}""")

valores = ['0 - 0.3',
           '0.3 - 0.5',
           '0.5 - 0.8',
           '0.8 - 1']
significado = ['Sem correlação',
               'Correlação fraca',
               'Correlação moderada',
               'Correlação forte']

int_corr = pd.DataFrame([valores,significado],
             index = ['Coeficiente r','Força']).T

st.write(int_corr)

sel_corr =  st.selectbox("Selecione uma feature",
                          num_stat_columns )


correlated_values = calcular_correlacao(df_preprocessed,
                                        num_stat_columns,
                                        sel_corr)

st.write(site_plot_corr(correlated_values))


st.markdown("""

- O número de visitantes no último mês ao site possuem uma correlação
    negativa, ou seja, :red-background[inversamente relacionada] à renda, renda per capita, e total gasto.
     Assim como a compra de carnes e em catálogos.

- O valor :green-background[total gasto] tem uma correlação forte em relação à compra de vinhos, carnes e compras em catálogos.


- A compra de :green-background[carnes e as compras feitas em catálogos] também possuem alta correlação.


- A :green-background[compra de vinhos] têm correlação média/forte com as compras na loja física e em catálogos.


""")


st.markdown("""
            ## Teste de chi quadrado
            É utilizado para verificar se existe uma :blue-background[associação entre duas variáveis categóricas]. Ele compara a distribuição observada 
            com a distribuição esperada, avaliando se as diferenças são significativas ou se podem ter ocorrido ao acaso.
""")

if on:
    st.latex(r'\chi^2 = \sum{\frac{(O_i - E_i)^2}{E_i}}')

col1, col2 = st.columns(2)

with col1:
    sel_chi_1 = st.selectbox("Selecione uma feature",
                            cat_stat_columns )
with col2:
    sel_chi_2 = st.selectbox("Selecione a feature para associação",
                            cat_stat_columns[::-1])

contingency_table, relatory_chi = site_calculate_chi2(df_preprocessed,
                     sel_chi_1,
                     sel_chi_2)

st.write(relatory_chi)

st.write(site_plot_chi(contingency_table))

st.markdown(
    """
    Os valores representados são os valores p que ficaram abaixo do threshold de :blue-background[$p = 0.05$], indicando que :green-background[há uma associação significativa] entre as variáveis.

Em termos de negócio as associações mais relevantes são:

- :orange-background[Recency]: A variável que está associada a quão recente o cliente fez a compra é "Response",
 indicando que a :green-background[probabilidade de resposta à campanha] varia com base em quão recentemente o cliente fez uma compra.

- :orange-background[Complain]: :red-background[As reclamações estão associadas à faixa etária] dos clientes.
 Sendo um indicativo da necessidade da análise das reclamações e apresentar um feedback apropriado para as faixas etárias de forma abrangente.

- :orange-background[Response]: Além de "Recency", ela está associada à educação, quantidade de crianças e adolescentes, e principalmente à quantidade de promoções ofertadas.
 Podemos interpretar que a última oferta que foi aceita :green-background[pode ter sido influenciada pelo número de ofertas totais anteriores].

"""
)

st.markdown("""
            ## Teste ANOVA

            ANOVA (Análise de Variância) é um teste estatístico que compara as médias de três ou mais grupos para verificar se há diferenças 
            significativas entre eles. Enquanto o teste t é usado para comparar duas médias, a ANOVA permite a comparação entre múltiplas médias 
            simultaneamente, sendo muito útil em experimentos onde se deseja testar diferentes tratamentos ou condições.
""")

if on:

    st.markdown(r"""
    | **Source of Variance**          | **Degree of Freedom (df)** | **Sum Square (SS)**                                                   | **Mean Square (MS)**               | **F-ratio**                     |
    |---------------------------------|----------------------------|------------------------------------------------------------------------|------------------------------------|---------------------------------|
    | **Between Groups (Treatment)**  | $k-1$                      | $SSB = \sum_{j=1}^{k} \frac{T_j^2}{n_j} - \frac{T^2}{n}$               | $MSB = \frac{SSB}{k-1}$            | $F = \frac{MSB}{MSW}$           |
    | **Within Groups (Error)**       | $n-k$                      | $SSW = \sum_{j=1}^{k} \sum_{i=1}^{n} (X_{ij} - \overline{X_j})^2$      | $MSW = \frac{SSW}{n-k}$            |                                 |
    | **Total**                       | $n-1$                      | $SST = \sum_{j=1}^{k} \sum_{i=1}^{n} (X_{ij} - \overline{X_t})^2$      |                                    |                                 |
    """)

sel_anova = st.selectbox("Selecione uma categoria",
                          cat_stat_columns)

df_anova = site_calculate_anova(df_preprocessed,
                    sel_anova,
                    num_stat_columns).style.apply(highlight_row,axis=1)

st.write(df_anova)

st.markdown("""
            Os p-values extremamente baixos sugerem que as variáveis categóricas
             como :orange-background[Education, Kidhome, Age, Teenhome, Response, e Promos_Total] têm um impacto
             estatisticamente significativo :green-background[sobre a maioria das variáveis numéricas].


""")