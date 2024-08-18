import sys
import os
import streamlit as st

diretorio_atual = os.getcwd()
diretorio_principal = os.path.dirname(diretorio_atual)
sys.path.insert(0, diretorio_principal)

image_cs = 'images/segmentation.png'
image_crisp = 'images/crispdm.png'
image_bip = 'images/biproblem.png'


st.title('Segmentação de clientes')

st.image(image_cs,caption='Segmentação de clientes')


st.markdown(
    """
    Nesse projeto será realizada uma aplicação de :blue-background[machine learning] para a segmentação de clientes baseado na técnica de clusterização,
      cujo a abordagem utiliza um **modelo de aprendizado não-supervisionado** para dividir em agrupamentos os dados que possuam :blue-background[características diferentes] entre si.
    """)



st.markdown("""
            ## Estrutura

            """)

st.image(image_crisp)


st.markdown("""
    
                
    A estrutura [CRISP-DM](https://docs.aws.amazon.com/whitepapers/latest/ml-best-practices-healthcare-life-sciences/machine-learning-lifecycle.html)
    foi utilizada como base para desenvolver esse trabalho, realizando a seguinte metodologia:

    1. Definir o problema de negócio.
    2. Coletar os dados e realizar análises preliminares dos mesmos.
    3. Aplicar etapas de pré-processamento: filtragem, tratamentos de dados e criação de *features*. 
    4. Realizar uma análise exploratória dos dados, detecção e remoção de outliers.
    5. Preparação dos dados para o modelo. 
    6. Divisão de clusters.
    7. Escolha do número ótimo de clusters.
    8. Testes no modelo final, avaliação e interpretação dos resultados.
    9. Implementar modelo.


"""
)

st.markdown("""## Problema de negócio""")

st.image(image_bip)

st.markdown("""
    Suponhamos que uma empresa está querendo promover estratégias de marketing para o lançamento de um determinado produto
    para todas as regiões disponíveis ao alcance almejando atingir **todo o seu público**, porém o custo de fabricação, transporte e marketing
    do produto podem não ter um retorno esperado em determinados setores, gerando assim uma :red-background[redução considerável na margem de lucro].
    Um modelo capaz de ler a base de dados dos clientes e :green-background[segmentar em diversos grupos] com base em suas preferências e características,
    pode :green-background[contornar gastos desnecessários] direcionando as estratégias utilizando de informações adicionais que possam auxilar nas tomadas de decisões comerciais.
""")