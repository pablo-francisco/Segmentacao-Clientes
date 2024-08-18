
import pickle

def save_as_pickle(path,name,file):
    """
    Salva arquivos em pickle.

    Input:
    path -- Caminho do diretório
    name -- Nome do arquivo pickle
    file -- Arquivo

    Output:
    None
    """

    with open(f'{path}\\{name}.pkl', 'wb') as f:
        pickle.dump(file, f)

def read_as_pickle(path,name):

    """
    Faz a leitura de arquivos pickle

    Input:
    path -- Caminho do diretório
    name -- Nome do arquivo pickle

    Output:
    file_out -- Arquivo
    
    """

    with open(f'{path}\\{name}.pkl', 'rb') as f:
        file_out = pickle.load(f)
    return file_out

def qtd_cat_distintas(df, categorical_personal):
    
    """
    Realiza a contagem de categorias distintas nos dados

    Input:
    df -- Dados de entrada
    categorical_personal --  Colunas de dados categóricos
    """
    
    for k in categorical_personal:
        print('-'*70)
        print(f'Valores distintos e suas quantidades para a variável "{k}"')
        print(df[k].value_counts())

