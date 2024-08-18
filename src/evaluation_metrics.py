
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import silhouette_samples
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import silhouette_score,davies_bouldin_score,calinski_harabasz_score
import numpy as np

from src.k_prototypes_model import clusterizar_dados_kprototypes

def plot_silhouette(X, clusters,title,cols_to_scatter):
    
    """
    Plota gráfico da distribuição do shilhouette score,
    e gráficos de dispersão 2D e 3D de features separados por clusters.

    Input:
    X -- Dados usados
    clusters -- Label com dados dos clusters respectivos
    title -- título do gráfico
    cols_to_scatter -- Colunas mostradas nos gráficos de dispersão

    Output:
    None
    """

    silhouette_vals = silhouette_samples(X, clusters)
    
    cluster_labels = clusters

    n_clusters = len(np.unique(clusters))
    
    fig = plt.figure(figsize=(24, 12))
    
    ax1 = fig.add_subplot(221)
    
    y_lower = 10
    # Shilhouette plot
    for i in range(n_clusters):
        cluster_silhouette_vals = silhouette_vals[clusters == i]
        cluster_silhouette_vals.sort()
        
        size_cluster_i = cluster_silhouette_vals.shape[0]
        y_upper = y_lower + size_cluster_i
        
        color = plt.cm.viridis(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_silhouette_vals,
                          facecolor=color, edgecolor=color, alpha=0.7)
        
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
        y_lower = y_upper + 10
        
    ax1.set_xlabel("Silhouette coeficient")
    ax1.set_ylabel("N° do Cluster")
    ax1.axvline(x=np.mean(silhouette_vals), color="red", linestyle="--")
    ax1.set_yticks([])
    ax1.set_title("Silhouette plot dos clusters")
    
    # ScatterPlot 2D
    ax2 = fig.add_subplot(223)
    scatter_plt = ax2.scatter(X[cols_to_scatter[0]], X[cols_to_scatter[1]], c=cluster_labels, cmap='viridis')

    legend = ax2.legend(*scatter_plt.legend_elements(), title="Clusters", loc="upper right")
    ax2.add_artist(legend)
    
    ax2.set_xlabel(f"Feature {cols_to_scatter[0]}")
    ax2.set_ylabel(f"Feature {cols_to_scatter[1]}")
    ax2.set_title("Scatter plot dos clusters")
    
    # ScatterPlot 3D
    ax3 = fig.add_subplot(122, projection='3d')
    scatter_3d = ax3.scatter(X[cols_to_scatter[0]], X[cols_to_scatter[1]],X[cols_to_scatter[2]], c=cluster_labels, cmap='viridis')
    legend_3d = ax3.legend(*scatter_3d.legend_elements(), title="Clusters", loc="upper right")
    ax3.add_artist(legend_3d)
    ax3.set_xlabel("Feature {}".format(cols_to_scatter[0]))
    ax3.set_ylabel("Feature {}".format(cols_to_scatter[1]))
    ax3.set_zlabel("Feature {}".format(cols_to_scatter[2]))
    ax3.set_title(f"Scatter plot 3D dos clusters")
    
    
    plt.suptitle(title,fontsize=24)
    plt.tight_layout()
    plt.show()
    
def silhouette_analysis(df,cat_columns,cluster_max,
                        save_path, gamma=None):
    
    """
    Realiza a análise de métricas para cada divisão de clusters.

    Input:
    df -- Dataframe utilizado
    cat_columns -- colunas categóricas
    cluster_max -- N° max de clusters da análise
    save_path -- Caminho onde será salva as métricas
    gamma -- Peso entre dados numéricos e categóricos  para a função de clusterização

    Output:
    silhouette_by_cluster -- silhouette score em cada divisão
    db_by_cluster -- davies bouldin score em cada divisão
    ch_by_cluster -- calinski harabasz score em cada divisão
    """

    clusters_vector = np.arange(2,cluster_max+1)
    silhouette_by_cluster = []
    ch_by_cluster = []
    db_by_cluster = []
    for K in clusters_vector:

 
        clusters,_ = clusterizar_dados_kprototypes(df,K,cat_columns,gamma=gamma)
        
        silhouette_avg = silhouette_score(df, clusters)
        db_scr = davies_bouldin_score(df, clusters)
        ch_score = calinski_harabasz_score(df, clusters)
        ch_by_cluster.append(ch_score)
        db_by_cluster.append(db_scr)
        silhouette_by_cluster.append(silhouette_avg)

        
        # Usando os clusters gerados anteriormente
        plot_silhouette(df, clusters,f"Análise para {K} clusters",['PC_1','PC_2','PC_3'])
        print('\n\n')
        
    df_temp_metrics = pd.DataFrame([silhouette_by_cluster,
              ch_by_cluster,db_by_cluster],
              index=['SC','CH','DB']).T
    df_temp_metrics['N° Cluster'] = np.arange(2,cluster_max+1)
    df_temp_metrics.to_csv(save_path)
    
    return silhouette_by_cluster,db_by_cluster,ch_by_cluster

def scores_plot(silhouette_by_cluster,ch_by_cluster,db_by_cluster):

    """
    Retorna o progresso de cada métrica por cluster.

    Input:
    silhouette_by_cluster -- silhouette score em cada divisão
    db_by_cluster -- davies bouldin score em cada divisão
    ch_by_cluster -- calinski harabasz score em cada divisão

    Output:
    None
    """
    scores = [silhouette_by_cluster,ch_by_cluster,db_by_cluster]
    title_names = ['Silhouette Score','C.H. Score','D.B. Score']
    fig, axs = plt.subplots(3,1,figsize=(12,6))
    for score,title,ax in zip(scores,title_names,axs):
        x_range = range(2,len(score)+2) 
        sns.lineplot(x = x_range ,y = score,marker='o',ax=ax)
        ax.set_xlabel('N° de clusters')
        ax.set_ylabel(title)
        ax.set_title(f'Gráfico do {title}')
    plt.tight_layout()
    plt.show()