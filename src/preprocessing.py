import pandas as pd
import numpy as np
import streamlit as st

def carregar_dados(path, parse_dates=None, sep=',', drop_col=None):
    """
    Carrega dados de um diretório.

    Keywords:
    path -- Diretório do arquivo
    parse_dates -- Transformação de coluna contendo datas (padrão None)
    sep -- Separador de arquivo usado (padrão ',')
    drop_col -- Eliminar coluna (padrão None)
    """
    
    df = pd.read_csv(path, sep=sep, parse_dates=parse_dates)
    if drop_col!= None:
        df = df.drop(drop_col, axis=1)
    return df

def preprocess_data(df, drop_columns, verbose=False):
    
    """
    Realiza o pré-processamento dos dados.

    Keywords:
    df -- Dados de entrada
    drop_columns -- Colunas a serem eliminadas dos dados
    verbose -- Apresentar prints e displays (padrão False)
    """
    
    df_preprocess = df.drop(drop_columns,axis=1)

    # Identificar quantidade de dados faltantes nas colunas em percentual
    colunas_nulas = round(100 * df_preprocess.isna().sum() / df_preprocess.shape[0],3).replace(0,np.nan).dropna().astype(str) + ' %'
    linhas_iniciais = df_preprocess.shape[0]
    df_preprocess = df_preprocess.dropna()
    
    if verbose==True:
        print(f'As colunas nulas e seu percentual são:')
        print(colunas_nulas)
        print(f'Um total de {linhas_iniciais - df_preprocess.shape[0] } linhas (clientes) foram removidas.')
        
    return df_preprocess

def categorize_numeric(df):
    
    """
    Divide os dados numéricos em categorias.

    Keywords:
    df -- Dados de entrada
    """
    
    # Demarcar divisões de classificações
    range_recency = [-1, 30, 60,
                     90, 365]
    labels_recency = ['1 Mes', '2 Meses',
                      '3 Meses', '> 3 Meses']
    
    range_age = [-1, 19, 45,
                 59, 200]
    labels_age = ['Jovens', 'Adultos',
                  'Meia-idade', 'Idosos']
    
    df_copia = df.copy()
    
    df_copia['Recency'] = pd.cut(x=df_copia['Recency'], bins=range_recency,
                                labels=labels_recency).astype(str)

    df_copia['Age'] = pd.cut(x=df_copia['Age'], bins=range_age,
                            labels=labels_age).astype(str)

    return df_copia


# @st.cache_data
def feature_engineering(df_preprocess):
    
    """
    Realiza a criação de novas features.

    Keywords:
    df_preprocess -- Dados de entrada pré-processados
    df_feature -- Dados com adição de novas features (Numéricas)
    df_feature_Cat -- Dados com adição de novas features (Categóricas)
    """

    df_feature = df_preprocess.copy()
    #Quantidade somada de promoções aceitas 
    df_feature['Promos_Total'] = df_feature[['AcceptedCmp1','AcceptedCmp2',
                                             'AcceptedCmp3','AcceptedCmp4',
                                             'AcceptedCmp5']].T.sum()

    #Idade na qual os dados foram coletados (2021)
    df_feature['Age'] = 2021 - df_feature['Year_Birth']

    #Quantidade de dependentes menores de idade.
    df_feature['Dependants'] = df_feature[['Kidhome','Teenhome']].T.sum()

    #A pessoa possui pelo menos um dependente menor de idade? (1 se sim, 0 caso contrário)
    df_feature['Has_minor'] = (df_feature['Dependants'] > 0).astype(int)

    #Há algum parceiros? (1: sim, 0: não)
    condicao_single = (df_feature['Marital_Status'] == 'Single')
    condicao_not_single = (df_feature['Marital_Status'] == 'Together')
    df_feature['Partner'] = (condicao_single | condicao_not_single).astype(int)

    #Total de pessoas na casa
    df_feature['House_members'] = df_feature[['Partner', 'Dependants']].T.sum() + 1

    #Renda per capita
    df_feature['Income_per_members'] = df_feature['Income'] / df_feature['House_members']

    #Total gasto
    df_feature['Total_spent'] = df_feature[['MntWines','MntFruits',
                                            'MntMeatProducts','MntFishProducts',
                                            'MntSweetProducts','MntGoldProds']].T.sum()

    # Filtragem e reclassificação no nível de escolaridade
    map_education = {"Basic":"Undergraduate", "2n Cycle":"Undergraduate",
                     "Graduation":"Graduate", "Master":"Postgraduate",
                     "PhD":"Postgraduate"}

    df_feature['Education'] = df_feature['Education'].map(map_education)

    # Removendo colunas redundantes após a criação de features
    df_feature = df_feature.drop(['Dt_Customer','Year_Birth','Marital_Status'],axis=1) 
    df_feature_cat = categorize_numeric(df_feature)

    return df_feature, df_feature_cat

def interquartil_bounds(df,column):
    """
    Faz o cálculos dos limites inferiores
    e superiores dos quartis

    Keywords:
    df -- Dados de entrada
    column -- Coluna alvo para o cálculo
    """
    
    data_temp = df[column].copy()
    Q1 = data_temp.quantile(.25)
    Q3 = data_temp.quantile(.75)
    
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5*IQR
    lower_bound = Q1 - 1.5*IQR
    
    return upper_bound, lower_bound
    
def remove_outlier(df,column):
    """
    Retorna valores com e sem outliers

    Keywords:
    df -- Dados de entrada
    column -- Coluna a serem removidos os outliers
    """
    
    data_temp = df[column].copy()
    upper_bound, lower_bound = interquartil_bounds(df,column)
    
    # Retorna valores sem outliers (no_out) e outliers (out)
    no_out = data_temp[(data_temp>=lower_bound) & (data_temp<=upper_bound)]
    out = data_temp[(data_temp<=lower_bound) | (data_temp>=upper_bound)]
    
    return no_out,out

def filter_outliers(df,verbose=False):
    
    """
    Remove os outliers por meio dos interquartis

    Keywords:
    df -- Dados de entrada
    verbose -- Apresentar prints e displays (padrão False)
    df_feature_no_out -- Dados com outliers filtrados
    df_feature_cat_no_out -- Dados com outliers filtrados (categóricos)
    """

    df_temp = df.copy()
    #Removidos os outliers das colunas 'Income' e 'Age'
    indices_outliers = remove_outlier(df_temp,'Income')[1].index.union(remove_outlier(df_temp,'Age')[1].index)
    df_feature_no_out = df_temp.drop(index=indices_outliers)
    df_feature_cat_no_out = categorize_numeric(df_feature_no_out)

    
    if verbose == True:
        
        num_outliers = len(indices_outliers)
        por_outliers = round(100*num_outliers / df_temp.shape[0], 2)
        
        print(f'A remoção de outliers reduziu os dados em {por_outliers}% ({num_outliers} clientes)')
    
    #Retorna dados antes e após a categorização dos dados numéricos (sem outliers)
    return df_feature_no_out, df_feature_cat_no_out

