

import sys
import os
from config import BASE_DIR
sys.path.insert(0, BASE_DIR)

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from src.utils import *



# diretorio_atual = os.getcwd()
# diretorio_principal = os.path.dirname(diretorio_atual)
# sys.path.insert(0, diretorio_principal)

def convert_object_to_num(df_temp):

    """
    Converte categorias str em numéricas.

    Input:
    df_temp -- Dataframe utilizado

    Output:
    df_preparation -- Dataframe convertido
    """

    df_preparation = df_temp.copy()

    #Converter as strings na coluna education para valores numéricos.
    num_map_edu = {'Graduate':1,'Postgraduate':2,'Undergraduate':0}
    num_map_age = {'Jovens':0, 'Adultos':1, 'Meia-idade':2,'Idosos':3}
    num_map_recency = {'1 Mes':0, '2 Meses':1, '3 Meses':2,'> 3 Meses':3}
    
    df_preparation['Education'] = df_preparation['Education'].map(num_map_edu)
    df_preparation['Age'] = df_preparation['Age'].map(num_map_age)
    df_preparation['Recency'] = df_preparation['Recency'].map(num_map_recency)
    return df_preparation

def escalonar_dados(df_tmp,all_cat,cat_relevant,load_file=False):
    
    """
    Escalona os dados numéricos.

    Input:
    df_temp -- Dataframe utilizado
    all_cat -- Todas as variáveis categóricas
    cat_relevant -- Variáveis categoricas usadas
    load_file -- Carregar dados de escalonamento do diretório

    Output:
    df_scaled -- Dataframe escalonado
    num_c --  Colunas numéricas
    """

    #modificar path
    # path_save_model = 'C:\\Users\\pablo\\OneDrive\\Área de Trabalho\\Data_projects\\MLops_test\\data\\data_transformation_tools'
    path_save_model = f'{BASE_DIR}\\data\\data_transformation_tools'

    # print(f'prep:{path_save_model}')
    
    name_file = 'std_scaler'
    
    if load_file==False:
    
        scaler_n = StandardScaler()
    else:
        scaler_n = read_as_pickle(path_save_model,name_file)


    num_c = df_tmp.drop(all_cat,axis=1).columns


    df_scaled_num = scaler_n.fit_transform(df_tmp[num_c])
    scaled_data = pd.DataFrame(df_scaled_num,columns=num_c)
    df_scaled = pd.concat([scaled_data,df_tmp[cat_relevant]],axis=1)

    if load_file==False:
        save_as_pickle(path_save_model,name_file,scaler_n)
    
    return df_scaled, num_c

def realizar_PCA(df_tmp,componentes,load_file=False):


    """
    Realiza as etapas de PCA salvando o modelo.

    Input:
    df_temp -- Dataframe utilizado
    componentes -- Número de componentes
    load_file -- Carregar dados de escalonamento do diretório

    Output:
    pca_df -- Dataframe com PCA realizado
    cumulative_variance_ratio -- Variância dos componentes
    pca_temp -- modelo do PCA utilizado
    """


    #modificar path
    # path_save_model = 'C:\\Users\\pablo\\OneDrive\\Área de Trabalho\\Data_projects\\MLops_test\\data\\data_transformation_tools'
    path_save_model = f'{BASE_DIR}\\data\\data_transformation_tools'

    # print(f'prep:{path_save_model}')


    name_file = 'PCA'
    
    if load_file==False:
        pca_temp = PCA(n_components=componentes,random_state=42)
        pca_data_temp = pca_temp.fit_transform(df_tmp)
    else:
        pca_temp = read_as_pickle(path_save_model,name_file)
        pca_data_temp = pca_temp.transform(df_tmp)
        
    pca_df = pd.DataFrame(data=pca_data_temp, columns=[f'PC_{x}' for x in range(1,1+pca_data_temp.shape[1])])
    cumulative_variance_ratio = np.cumsum(pca_temp.explained_variance_ratio_)
    return pca_df,cumulative_variance_ratio,pca_temp

def otimizar_PCA(df_tmp,var_necessaria,
                 pca_init=None,plot_graph=True):
    
    """
    Encontra o número de componentes
    necessários que satisfaçam a variância desejada.

    Input:
    df_temp -- Dataframe utilizado
    var_necessaria -- Variância mínima necessária dos componentes
    pca_init -- N° inicial de componentes
    plot_graph -- Gráfico da variância cumulativa por N° de componentes


    Output:
    pca_df -- Dataframe com PCA realizado
    pca_temp -- modelo do PCA utilizado
    """

    if pca_init == None:
        pca_init = df_tmp.shape[1] - 1
        
    pca_df,cumulative_variance_ratio,pca_temp = realizar_PCA(df_tmp,pca_init)

    # Encontrando o número de componentes necessários para reter X% da variância
    n_components_necessarios = np.argmax(cumulative_variance_ratio >= var_necessaria) + 1
    
    
    if plot_graph == True:
        
        x_range = np.arange(1,pca_init+1,1)

        fig,ax = plt.subplots(1,1,figsize=(16,8))

        sns.lineplot(y=cumulative_variance_ratio,marker='o',label='Variância cumulativa',x=x_range)
        ax.axvline(n_components_necessarios,ymin=0,ymax=1.1,color='#e85d04',ls='--',label=f'Variância de {100*var_necessaria}%')
        ax.set_xticks(x_range)
        ax.set_xlabel('N° de componentes')
        ax.set_ylabel('Variância')
        ax.legend()
        plt.show()


    if pca_init != n_components_necessarios:
        pca_df,cumulative_variance_ratio,pca_temp = realizar_PCA(df_tmp,n_components_necessarios)

    else:
        pass

    return pca_df,pca_temp
   

    
def PCA_on_numeric(df,numeric_columns,cat_used,exp_variance,plot_graph=True):
    
    """
    Realiza a operação de PCA nos dados numéricos retornando
    os dados já tratados em conjunto com os categóricos, 
    além de salvar o modelo de PCA.

    Input:
    df_temp -- Dataframe utilizado
    var_necessaria -- Variância mínima necessária dos componentes
    pca_init -- N° inicial de componentes
    plot_graph -- Gráfico da variância cumulativa por N° de componentes

    Output:
    pca_df -- Dataframe com PCA realizado
    pca_temp -- modelo do PCA utilizado
    """

    
    pca_data,pca_temp = otimizar_PCA(df[numeric_columns],exp_variance,plot_graph=plot_graph)
    df_preparation_reducted= pd.concat([df[cat_used],pca_data],axis=1)
    
    # path_save_model = 'C:\\Users\\pablo\\OneDrive\\Área de Trabalho\\Data_projects\\MLops_test\\data\\data_transformation_tools'
    
    path_save_model = f'{BASE_DIR}\\data\\data_transformation_tools'

    # print(f'prep:{path_save_model}')


    name_file = 'PCA'
    

    save_as_pickle(path_save_model,name_file,pca_temp)
    
    return df_preparation_reducted

def dimensionality_reduction(df_scaled,numeric_columns,
                             cat_used,exp_variance,load_PCA,
                             plot_graph=False):
    
    """
    Uma pipeline condensando
    as funções de redução de dimensionalidade.

    Input:
    df_scaled -- Dataframe escalonado
    exp_variance -- Variância mínima necessária dos componentes
    numeric_columns -- Features numéricas
    cat_used -- Features categóricas
    plot_graph -- Gráfico da variância cumulativa por N° de componentes
    load_PCA -- Usar modelo PCA já salvo
    
    Output:

    df_preparation_reducted -- Dados com redução de dimensionalidade aplicada
 
    """

    if load_PCA == False:
        df_preparation_reducted = PCA_on_numeric(df_scaled,
                                                 numeric_columns,
                                                 cat_used,exp_variance,
                                                 plot_graph=plot_graph)

    else:
        pca_data, _, _ = realizar_PCA(df_scaled[numeric_columns]
                                      ,None,load_file=True)
        
        df_preparation_reducted= pd.concat([df_scaled[cat_used]
                                            ,pca_data],axis=1)
    
    return df_preparation_reducted