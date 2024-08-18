import sys
import os
import streamlit as st

diretorio_atual = os.getcwd()
diretorio_principal = os.path.dirname(diretorio_atual)
sys.path.insert(0, diretorio_principal)



st.markdown("""
            # Estratégias baseadas nos dados

            Após as verificações dos testes estatísticos sobre os dados e possíveis relações entre variáveis,
            podem se tomar as seguintes pautas em reuniões para discutir sobre :blue-background[estratégias que melhorem a experiência
            do cliente] ao mesmo tempo em que incrementa os lucros da empresa.


            ## Tópico 1 - Como usaremos a alta demanda de produtos de luxo, como o vinho e a carne, ao nosso favor? 

            Tendo em vista que esses produtos são comprados por pessoas com :blue-background[alta renda e altos gastos], e a correlação destes
            produtos com o total que foi gasto em todos os produtos é alta, seria recomendado uma :green-background[abordagem de marketing voltado à
            esses dois produtos], e que as :green-background[promoções sejam repassadas mais de uma vez], pois segundo o perfil dos consumidores de alta classe
            aceitaram mais de uma promoção. Evidentemente o meio em que esses produtos são comprados deve ser levado em consideração, que
            no caso são comprados por meio de catálogos, indicando que as :green-background[compras em lojas físicas são preferíveis para esses consumidores],
            porém é o meio de compra menos frequente em comparação aos demais, seria necessária uma análise mais detalhada das informações sobre
            os estabelecimentos.

            ## Tópico 2 - Como devemos abordar as nossas ofertas?

            A resposta à uma oferta fornecida pela campanha de marketing está associada ao período da última compra feita pelos clientes, ou seja,
            devemos :green-background[realizar ofertas em um período que os clientes estejam mais confortáveis] para uma nova compra, porém não deve-se esperar demais
            para não prejudicar as chances da oferta ser aceita. O número de ofertas anteriores que foram aceitas pelos clientes também são um fator
            que está associado, onde uma pessoa com um histórico de aceitar mais promoções tende a continuar nesse ritmo, nesse caso :green-background[deve-se
            ofertar para clientes que vem com uma sequência de compras a partir das ofertas.]

            ## Tópico 3 - A imagem da empresa, assim como a qualidade dos produtos está em níveis satisfatórios?

            A taxa de reclamações dos produtos da empresa está :green-background[abaixo de 1%], então é um nível considerado dentro da normalidade. Porém o recomendado
            é sempre tentar zerar esse valor, a única relação significativa com a taxa de reclamações é a :blue-background[faixa etária] onde pode haver vários fatores
            envolvidos, provavelmente apenas a individualidade e experiência de cada cliente, mas :blue-background[uma análise sobre as reclamações deve ser realizada]
            para garantir o máximo de conforto às pessoas.

""")


st.markdown("***")

st.markdown("""
# Análise de incremento no ROI

Este projeto tem como objetivo fornecer insights que ajudem
a :green-background[aumentar a margem do ROI atual das campanhas de marketing]
para um produto específico e estimar o ROI esperado com a 
implementação de um modelo de segmentação de clientes.

## O que é ROI e sua importância?
O ROI (Return on Investment), ou Retorno sobre o Investimento,
é uma métrica financeira que :green-background[mede a eficácia de um investimento].
Ele é calculado como a razão entre o lucro líquido obtido com o
investimento e o custo do investimento. O ROI é importante porque permite avaliar a eficiência e a rentabilidade
de um investimento, facilitando a comparação entre diferentes oportunidades de investimento e ajudando a tomar decisões informadas para maximizar os retornos financeiros.

""")

st.markdown("""
## Estrutura de cálculo de custos.

### Custos atuais

Iniciando pelos custos de criação e divulgação da campanha que geralmente seguem a estrutura:

1. Uso de plataformas de divulgação como o Google Ads ou Facebook Ads
    - Custo por Clique (CPC)
    - Custo por Mil Impressões (CPM)
    - Custo por Aquisição (CPA)

2. Produção de conteúdo de marketing
    - Design gráfico
    - Produção e edição de vídeos

3. Gestão e otimização:

    - Testes A/B
    - Monitoramento da campanha
    - Insights sobre os dados

### Custos utilizando a segmentação de clientes

Para a implementação do modelo de segmentação de clientes,
os testes para os custos :blue-background[devem ser realizados em múltiplas campanhas] sendo
preferencialmente uma para cada cluster, para :green-background[avaliar adequadamente] a implementação do modelo aplicado.

A estrutura de custos é dada abaixo como:

1. Custo de implementação e manutenção do modelo.
2. Cálculo de custos em campanhas aplicadas à diferentes clusters.


""")


st.markdown("""
## Análise do ROI

Após as etapas dos cálculos de custos, é realizada uma análise do ROI nos
diferentes cenários e se há viabilidade de manter o projeto em vigor conforme 
os resultados obtidos.

""")
