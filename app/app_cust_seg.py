
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title='Projeto de segmentação')


placeholder = st.empty()
with placeholder.container():

    Intro_page = st.Page('pages/Intro.py',
             title="Homepage",
             default=True,
             icon=':material/home:')
    
    data_page = st.Page('pages/Data_infos.py',
             title="Sobre os dados", 
             icon=':material/database:')

    EDA_page = st.Page('pages/Plotting_Data.py',
             title="Análise exploratória", 
             icon=':material/monitoring:')
    
    Cluster_page = st.Page('pages/Plotting_Cluster.py',
             title="Análise de Clusters",
             icon=':material/join:')
    
    Metrics_page = st.Page('pages/Plotting_metrics.py',
             title="Métricas do modelo",
             icon=":material/bar_chart:")
    
    Strategies_page = st.Page('pages/Strategies.py',
             title="Estratégias de negócio",
             icon=":material/payments:"
             )
    
    Stats_page = st.Page('pages/Statistical_analysis.py',
             title="Statistical Analysis",
             icon=":material/query_stats:"
             )
    
    Insights_page = st.Page('pages/Insights_EDA.py',
             title="Insights",
             icon=":material/search:"
             )
    
    pg = st.navigation(
        {
            "Início": [Intro_page,data_page],
            "Análises": [EDA_page,Stats_page],
            "Modelo": [Cluster_page,Metrics_page],
            "Business Inteligence": [Insights_page, Strategies_page]
            
        }
    )

    pg.run()