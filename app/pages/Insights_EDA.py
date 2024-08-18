import sys
import os
import streamlit as st

diretorio_atual = os.getcwd()
diretorio_principal = os.path.dirname(diretorio_atual)
sys.path.insert(0, diretorio_principal)

st.markdown(""" 
            # Quais informações úteis podemos extrair?
""")

st.markdown("""
            ## Análise exploratória dos dados
            
            Utilizando os gráficos de dispersão, nota-se que:
            
            - Os clientes que não possuem filhos gastam mais em carnes
            - Os que possuem gastam mais em vinhos
            - Pessoas com renda acima de aproximadamente 50K
             aumentam seu poder de compra em todos os produtos.
            - Clientes com renda abaixo de aproximadamente 50K aceitaram a apenas uma promoção
            
            Com isso podemos concluir que:

            Um sistema de recomendação de produtos pode ser
            alimentado com as informações sobre os :green-background[vinhos e carnes],
            pois possuem relações diretas nítidas.

            A estratégia de realizar :green-background[mais de uma promoção] é mais vantajosa
            para clientes com :green-background[alta renda e altos gastos].
            
            As compras por catálogo são realizadas com :red-background[menores frequências] em relação à
            outros meios, o que indica que o ROI pode ser menor que a margem esperada.

            """)

st.markdown("""
            ## Análise estatística

            ### Variáveis numéricas
            
            -  Clientes com maior renda :red-background[tendem a visitar menos o site], sugerindo que eles podem estar mais inclinados a comprar diretamente em lojas
                    físicas ou através de outros canais, como catálogos. Isso também pode indicar que esses clientes valorizam mais a
                    experiência de compra offline ou em canais mais personalizados.

            - Clientes que gastam mais em geral :green-background[tendem a investir] significativamente em produtos de alto valor, como :green-background[vinhos e carnes], e fazem compras
                    substanciais por catálogo. Isso pode indicar uma preferência por produtos premium e um estilo de vida mais gourmet.

            - Clientes que compram :green-background[carnes] também têm uma forte tendência a :green-background[utilizar catálogos] para fazer compras.
                 Isso pode indicar que eles valorizam a conveniência e a capacidade de planejar suas compras de alimentos com antecedência.

            - Clientes que compram :green-background[vinhos] parecem preferir a experiência de escolha pessoal que uma :green-background[loja física] oferece ou a conveniência de selecionar vinhos em catálogos detalhados.
                 Esse comportamento sugere que esses clientes podem valorizar tanto a experiência de compra física quanto a conveniência dos catálogos.

            ### Variáveis categóricas

            - :orange-background[Recency]: A variável que está associada a quão recente o cliente fez a compra é "Response", indicando que a :green-background[probabilidade de resposta] à campanha
                        varia com base em quão :green-background[recentemente o cliente fez uma compra].

            - :orange-background[Complain]: As :red-background[reclamações estão associadas à faixa etária] dos clientes.
                        Sendo um indicativo da necessidade da análise das reclamações e apresentar um feedback apropriado para as faixas etárias de forma abrangente.

            - :orange-background[Response]: Além de "Recency", ela está associada à educação, quantidade de crianças e adolescentes, e principalmente à quantidade de promoções ofertadas.
                        Podemos interpretar que a última oferta que foi aceita pode ter sido influenciada pelo número de ofertas totais anteriores.


            ### Variáveis categóricas e numéricas

            
            O teste ANOVA indica que as variáveis importantes estão apresentadas abaixo:

            
            - :orange-background[Education]
            - :orange-background[Kidhome]
            - :orange-background[Age]
            - :orange-background[Teenhome]
            - :orange-background[Response]
            - :orange-background[Promos_Total]

            Na qual devem ser considerados durante a estratégias de marketing para uma maior compra de produtos em geral,
            tanto em gastos quanto em locais usados durante as transações, como as compras online por exemplo.
            
""")