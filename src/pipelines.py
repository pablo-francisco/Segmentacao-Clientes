

import sys
import os

from config import BASE_DIR
sys.path.insert(0, BASE_DIR)

from src.preprocessing import *
from src.utils_EDA import *
from src.utils import *
from src.preparation import *
from src.k_prototypes_model import *
from src.evaluation_metrics import *



def pipeline_preprocessing(df, filter_out=True):
    """
    Realiza a etapa de pré-processamento.

    Input:
    df -- Dados de entrada
    filter_out  -- filtrar outliers (padrão True)

    Output:
     df_feature -- Dados com adição de novas features (Numéricas)
    df_feature_Cat -- Dados com adição de novas features (Categóricas)

    """

    df_preprocess = preprocess_data(df, ['Z_CostContact','Z_Revenue','ID'])
    df_feature, df_feature_cat = feature_engineering(df_preprocess)

    if filter_out == True:
        df_feature, df_feature_cat = filter_outliers(df_feature)

    return df_feature, df_feature_cat



def pipeline_preparation(df,cat_used,load_scaler=False,load_PCA=False):
    
    """
    Pipeline da etapa de preparação dos dados.

    Input:
    df -- Dados de entrada
    cat_used -- Features categóricas que serão usadas no modelo
    load_scaler -- Carregar arquivo com o escalonador usado (padrão False)
    load_PCA -- Carregar arquivo com o PCA usado (padrão False)

    Output:
    df_preparation_reducted - Dados com redução de dimensionalidade aplicada

    """
    all_cat = ['Age','Recency','Promos_Total','Education','AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1',
           'AcceptedCmp2', 'Complain', 'Response', 'Partner','Kidhome', 'Teenhome','Dependants','Has_minor','House_members']
    std_pca = .9

    df_preparation = convert_object_to_num(df)
    df_scaled, num_c = escalonar_dados(df_preparation,all_cat,cat_used,load_file=load_scaler)
    df_preparation_reducted = dimensionality_reduction(df_scaled,num_c,cat_used,std_pca,load_PCA,plot_graph=False)

    return df_preparation_reducted


def pipeline_clusterize(df,cat_used,K,load_scaler=False,load_PCA=False,
                        ):

        
    """
    Pipeline final para o modelo de clusterização.

    Input:
    df -- Dados de entrada
    cat_used -- Features categóricas que serão usadas no modelo
    K -- Número de clusters a serem formados
    load_scaler -- Carregar arquivo com o escalonador usado (padrão False)
    load_PCA -- Carregar arquivo com o PCA usado (padrão False)

    Output:
    df_final -- Dados clusterizados
    model -- Modelo utilizado

    """

    df_temp = df.copy()
    



    path_save_model = f'{BASE_DIR}\\data\\models'
    path_preparation = f'{BASE_DIR}\data\\prepared\\marketing_campaign_prepared.csv'
    path_preprocess = f'{BASE_DIR}\data\\processed\\marketing_campaign_processed.csv'
    path_final = f'{BASE_DIR}\data\\clustered\\marketing_campaign_clustered.csv'
    
    
    df_1 = pipeline_preprocessing(df_temp,filter_out=True)[1].reset_index(drop=True)
    
    df_1.to_csv(path_preprocess)
    
    df_2 = pipeline_preparation(df_1,cat_used,load_scaler=load_scaler,load_PCA=load_PCA)
    df_2.to_csv(path_preparation)
    
    df_final,model = fit_pred_data(df_1,df_2,K,cat_used)
    df_final.to_csv(path_final)
    
    name_file = 'kprototypes'
    save_as_pickle(path_save_model,name_file,model)
    
    
    return df_final,model

