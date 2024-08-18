
import streamlit as st

import sys
import os
# diretorio_atual = os.getcwd()
# sys.path.insert(0, diretorio_atual)
from config import BASE_DIR
sys.path.insert(0, BASE_DIR)

from app.utils import *
from src.preprocessing import carregar_dados




path = f'{BASE_DIR}\\data\\raw\\marketing_campaign.csv'

df_temp1, _ , _ = relevant_data(K = 2)


df = carregar_dados(path,parse_dates=['Dt_Customer'],sep='\t',drop_col=None)
 
st.markdown("""
            # Informações sobre os dados
            
            Os dados foram coletados da plataforma [Kaggle](https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis)
            e utilizados como um estudo de caso para entender o comportamento dos clientes.

            """)


st.markdown('## Dicionário de dados')

st.markdown("""
:blue-background[Pessoal]
* :orange-background[ID]: Número de identificação único do cliente;
* :orange-background[Year_Birth]: Ano de nascimento;
* :orange-background[Education]: Nível de escolaridade;
* :orange-background[Marital_Status]: Estado civil;
* :orange-background[Income]: Renda anual familiar;
* :orange-background[Kidhome]: Número de crianças na residência do cliente;
* :orange-background[Teenhome]: Número de adolescentes na residência do cliente;
* :orange-background[Dt_Customer]: Data de cadastro do cliente na empresa;
* :orange-background[Recency]: Número de dias desde a última compra do cliente;
* :orange-background[Complain]: Indicação se o cliente reclamou pelo menos uma vez nos últimos 2 anos.
***
:blue-background[Produtos]
* Pré-fixo **Mnt** indica a quantidade de dinheiro gasto com o produto nos últimos 2 anos:
    * :orange-background[MntWines]: Gastos com vinho;
    * :orange-background[MntFruits]: Gastos com frutas;
    * :orange-background[MntMeatProducts]: Gastos com carnes;
    * :orange-background[MntFishProducts]: Gastos com peixes;
    * :orange-background[MntSweetProducts]: Gastos com doces;
    * :orange-background[MntGoldProds]: Gastos com ouro.
***
:blue-background[Promoções]
* :orange-background[NumDealsPurchases]: Número de compras feitas com desconto;
* :orange-background[AcceptCmp1 - AcceptCmp5]: Aceitação do cliente na oferta de N° correspondente ao sufixo (1 caso aceito, caso contrário 0);
* :orange-background[Response]: Se o cliente aceitou a oferta na ultima campanha.
***
:blue-background[Locais de compra]
* :orange-background[NumWebPurchases]: Número de compras feitas pelo site da empresa;
* :orange-background[NumCatalogPurchases]: Número de compras feitas usando um catálogo;
* :orange-background[NumStorePurchases]: Número de compras feitas diretamente na loja;
* :orange-background[NumWebVisitsMonth]: Número de visitas ao site da empresa no último mês.
***
:blue-background[Demais variáveis]

As variáveis :orange-background[Z_CostContact e Z_Revenue] não foram documentadas informações que indicassem os seus significados ou importâncias das mesmas, posteriormente na análise exploratória será dada importância a tentar explicar essas variáveis, e se são relevantes para nosso objetivo. 

""")

st.markdown('## Dados puros')

st.write(df)

st.markdown('## Dados pré-processados')

st.write(df_temp1)

