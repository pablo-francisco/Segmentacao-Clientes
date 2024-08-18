import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import seaborn as sns
from src.preprocessing import remove_outlier
import pandas as pd
from scipy import stats


def set_graph_configs(lw=1, fs=12, color_palette=['#45056e', '#e85d04', '#7a057e', '#ff8200', '#a64ed1', '#ff9c33']):

    """
    Realizar a configuração das ferramentas gráficas (matplotlib e seaborn).

    Input:
    
    lw -- Tamanho de linhas (padrão 1)
    fs -- Tamanho da fonte (padrão 12)
    color_palette -- Paleta de cores usadas (padrão ['#45056e', '#e85d04', '#7a057e', '#ff8200', '#a64ed1', '#ff9c33']) 
    """

    
    mpl.style.use('ggplot') 
    mpl.rcParams['axes.facecolor']      = 'white'
    mpl.rcParams['axes.linewidth']      = lw
    mpl.rcParams['xtick.color']         = 'black'
    mpl.rcParams['ytick.color']         = 'black'
    mpl.rcParams['grid.color']          = 'lightgray'
    mpl.rcParams['figure.dpi']          = 150
    mpl.rcParams['axes.grid']           = True
    mpl.rcParams['font.size']           = fs


    sns.set_palette(sns.color_palette(color_palette))
    sns.color_palette(color_palette)
    

def graph_categorical(df,lista_categoricas):
    
    """
    Realiza barplots de dados categóricos

    Input:
    
    df -- Dados de entrada
    lista_categoricas --  Colunas de dados categóricos
    """
    
    for k in lista_categoricas:
        
        #Converte os valores em percentual
        dist_dados = 100*df[k].value_counts() / df[k].value_counts().sum()
        dist_dados = dist_dados.to_frame().reset_index()
        dist_dados.columns = [k,'Quantidade (%)']

        fig, ax = plt.subplots(1,1,figsize=(8, 6))

        sns.barplot(data=dist_dados,x=k,y='Quantidade (%)',ax=ax)

        for bar in ax.patches:
            height = bar.get_height()
            ax.annotate('{:.1f}%'.format(height), 
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 10),  
                        textcoords="offset points",
                        ha='center', va='center',
                        fontsize=11, color='black')
            
        ax.set_title(f'Distribuição da variável "{k}"')
        ax.set_ylim(0,110)
        plt.tight_layout()
        plt.show()
        
        print('-'*125)

def hist_graph(df,lista_num):
    
    """
    Realiza histogramas de dados numéricos

    Input:
    
    df -- Dados de entrada
    lista_num --  Colunas de dados numéricos
    """
    
    for col1,col2 in zip(lista_num[:-1:2],lista_num[1::2]):
        fig, ax = plt.subplots(1,2,figsize=(16, 8))

        for i,k in enumerate([col1,col2]):
            sns.histplot(data=df[k],ax=ax[i],bins=150,kde=True)
            ax[i].set_title(f'Histograma de "{k}"')
            ax[i].set_ylabel('Quantidade')
            ax[i].set_xticklabels(ax[i].get_xticklabels(), rotation=45)


        plt.tight_layout()
        plt.show()
        print('-'*125)

        
def boxplot_outliers(df,lista_num):
    
    """
    Realiza boxplots de dados numéricos
    com e sem outliers

    Input:
    
    df -- Dados de entrada
    lista_num --  Colunas de dados numéricos
    """
    
    
    for feature_analisada in lista_num:

        fig, ax = plt.subplots(1,2,figsize=(16,8))

        dados_temp = [df[feature_analisada],remove_outlier(df,feature_analisada)[0].reset_index(drop=True)]
        titles = ['Normal','Sem outliers (Redução pelo método de interquartis)']

        for i,out_value in enumerate(dados_temp):

            sns.boxplot(out_value,ax=ax[i])
            ax[i].set_title(f'{titles[i]}')

        fig.suptitle(f'Boxplot dos dados de "{feature_analisada}"',fontsize=16)
        plt.tight_layout()
        plt.show()

        print('-'*125)
    
def pairplots(df,x_y,hue_features):
    
    """
    Realiza gráficos de densidade
    e disperão dos dados

    Input:
    
    df -- Dados de entrada
    x_y --  Colunas numéricas cujo serão apresentadas na análise multivariada
    hue_features -- Colunas categóricas a serem destacadas na análise
    """
    
    for hue in hue_features:
        markers=["o", "s", "D","x"]
        marker = markers[:len(df[hue].unique())]
        sns.pairplot(df[x_y+[hue]],hue=hue,markers=marker)
        plt.show()
        print('-'*125)
        print('\n')   

def graph_categorical_clusters(df_final,lista_categoricas):
    
    """
    Realiza gráficos de barra dos dados separados por clusters

    Input:
    
    df_final -- Dados de entrada
    lista_categoricas --  Colunas categóricas usadas
    """

    for k in lista_categoricas:
        dist_dados = (100*df_final.groupby([k,'Clusters']).size()/df_final.shape[0]).reset_index()
        dist_dados.columns = list(dist_dados.columns[:-1]) + ['Quantidade (%)']

        fig, ax = plt.subplots(1,1,figsize=(8, 6))


        sns.barplot(data=dist_dados,x=k,y='Quantidade (%)',ax=ax,hue='Clusters')

        for bar in ax.patches:
            height = bar.get_height()
            ax.annotate('{:.1f}%'.format(height), 
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 10),  
                        textcoords="offset points",
                        ha='center', va='center',
                        fontsize=10, color='black')
        ax.set_title(f'Distribuição da variável "{k}"')


        plt.tight_layout()
        plt.show()

        print('-'*125)

def boxplot_clusters(df_final,lista_num):

    """
    Realiza gráficos de caixa dos dados separados por clusters

    Input:
    
    df_final -- Dados de entrada
    lista_num --  Colunas numéricas usadas
    """

    for feature_analisada1,feature_analisada2 in zip(lista_num[::2],lista_num[1::2]):


        fig, ax = plt.subplots(1,2,figsize=(16,8))

        dados_temp = [df_final[[feature_analisada1,'Clusters']],
                      df_final[[feature_analisada2,'Clusters']]]
        titles = [f'Boxplot de "{feature_analisada1}"',f'Boxplot de "{feature_analisada2}"']

        for i,out_value in enumerate(dados_temp):
            sns.boxplot(data=out_value,ax=ax[i],y=out_value.columns[0],x='Clusters',showfliers=False)
            ax[i].set_title(f'{titles[i]}')

        plt.tight_layout()
        plt.show()

        print('-'*125)



def correlation_plot_EDA(df,columns,threshold=0.5):
    
    """
    Realiza gráficos de calor indicando as correlações numéricas

    Input:
    
    df -- Dados de entrada
    columns --  Colunas numéricas usadas
    threshold -- Apresentar correlação acima de um valor absoluto
    """

    corr_matrix = df[columns].corr()

    fig, ax = plt.subplots(1,1,figsize=(12,8))


    if threshold is not None:
        filtered_corr_matrix = corr_matrix[(corr_matrix.abs() >= threshold) & (corr_matrix.abs() != 1)]
        plt.title(f"Correlação de pearson (threshold > {threshold})")

    else:
        filtered_corr_matrix = corr_matrix
        plt.title(f"Correlação de pearson")


    sns.heatmap(filtered_corr_matrix,
                cmap = 'coolwarm',
                annot=True,
                ax=ax)
    plt.tight_layout()
    plt.show()

def chi2_heatmap(df_temp,cat_columns):

    """
    Realiza gráficos de calor indicando as associações entre categorias

    Input:
    
    df_temp -- Dados de entrada
    cat_columns --  Colunas categoricas usadas
    """

    p_values_df = pd.DataFrame(index=cat_columns, columns=cat_columns)

    # Realizando o teste Qui-Quadrado para cada par de colunas categóricas
    for i in range(len(cat_columns)):
        for j in range(i + 1, len(cat_columns)):
            col1 = cat_columns[i]
            col2 = cat_columns[j]
            
            contingency_table = pd.crosstab(df_temp[col1], df_temp[col2])
            
            # Aplicando o teste Qui-Quadrado
            _, p, _, _ = stats.chi2_contingency(contingency_table)
            
            # Armazenando os valores de p no dataframe
            p_values_df.loc[col1, col2] = p
            p_values_df.loc[col2, col1] = p  # Para garantir simetria na matriz

    df_p = p_values_df[(p_values_df < .05) & (p_values_df > 0)]
    df_p = df_p.where(pd.notna(df_p), None).astype(float)
    

    fig, ax = plt.subplots(1,1,figsize=(12,6))
    sns.heatmap(df_p,
                cmap = 'coolwarm',
                annot=True,
                ax=ax)
    
    plt.title("Teste chi-squared para as  variáveis categóricas")
    plt.tight_layout()
    plt.show()


def anova_heatmap(df_temp,
                  numerical_columns,
                  categorical_columns):
    
    """
    Realiza gráficos de calor indicando as associações
    variáveis categóricas e numéricas.

    Input:
    
    df_temp -- Dados de entrada
    categorical_columns --  Colunas categoricas usadas
    numerical_columns -- Colunas numéricas usadas
    """
    
    anova_results = pd.DataFrame(index=categorical_columns, columns=numerical_columns)

    # Loop através de cada combinação de colunas categóricas e numéricas
    for cat_col in categorical_columns:
        for num_col in numerical_columns:
            
            # Aplicar ANOVA para cada combinação
            groups = [df_temp[num_col][df_temp[cat_col] == category] for category in df_temp[cat_col].unique()]
            anova_result = stats.f_oneway(*groups)
            
            anova_results.loc[cat_col, num_col] = anova_result.pvalue

    anova_results = anova_results.astype(float)

    anova_p = anova_results[(anova_results < .05) & (anova_results > 0)]
    anova_p = anova_p.where(pd.notna(anova_p), None).astype(float)


    fig, ax = plt.subplots(1,1,figsize=(14,8))
    sns.heatmap(anova_p,
                cmap = 'coolwarm',
                annot=True,
                ax=ax)
    plt.title("Teste ANOVA para as  variáveis")
    plt.tight_layout()
    plt.show()