import os
import sys
from config import BASE_DIR

sys.path.insert(0, BASE_DIR)
# diretorio_atual = os.getcwd()
# diretorio_principal = os.path.dirname(diretorio_atual)


from src.pipelines import *
from src.preprocessing import carregar_dados
import streamlit as st


  
@st.cache_data
def relevant_data(K=5):
    path = f'{BASE_DIR}\data\\raw\\marketing_campaign.csv'
    df = carregar_dados(path,parse_dates=['Dt_Customer'],sep='\t',drop_col=None)

    cat_relevant = ['Age','Recency','Promos_Total',
                    'Education','Complain', 'Response', 
                    'Partner','Kidhome', 'Teenhome']


    df_out, model = pipeline_clusterize(df,cat_relevant,K)
    df_temp1 = pipeline_preprocessing(df, filter_out=True)[1].reset_index(drop=True)
    df_temp2 = pipeline_preparation(df_temp1, cat_relevant)
    df_temp3 = pd.concat([df_temp2, df_out['Clusters']],axis=1)
    return df_temp1, df_out, df_temp3