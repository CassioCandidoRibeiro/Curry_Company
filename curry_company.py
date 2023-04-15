################################################
# Bibliotecas
################################################

# Manipulação dos dados
import pandas as pd

# Gráficos
import plotly.express as px

# Mapa
import folium

# Arquivo de funções (ferramentas.py)
import ferramentas as fr

# Streamlit para visualização web
import streamlit as st
from streamlit_folium import folium_static

################################################
# Upload e limpeza dos dados
################################################

df = pd.read_csv('curry.csv')
df = fr.limpeza_dos_dados(df)

################################################
# Streamlit Configuração da Página
################################################

st.set_page_config(
    page_title="Empresa", 
    page_icon="logo.png", 
    menu_items=None,
    layout="wide"
    )

################################################
# Streamlit Sidebar
################################################
# Logo da empresa
################################################

st.sidebar.image('logo.png', width=300)
st.sidebar.write('---')

################################################

################################################
# Filtros:
################################################
# 1. Densidade de tráfego
# 2. Tipo de área
# 3. Condição climática  
################################################

# 1. Densidade de tráfego
filtro_de_trafego = st.sidebar.multiselect(
    'Densidade de tráfego:',
    ['Baixo','Médio','Alto','Engarrafado'],
    default=['Baixo','Médio','Alto','Engarrafado'])

# 2. Tipo de área
filtro_de_area = st.sidebar.multiselect(
    'Tipo de área:',
    ['Urbana','Semi-urbana','Metropolitana'],
    default=['Urbana','Semi-urbana','Metropolitana'])

# 3. Condição climática
filtro_de_clima = st.sidebar.multiselect(
    'Condição climática:',
    ['Ensolarado','Nublado','Nebuloso','Ventoso','Tempestuoso','Tempestades de areia'],
    default=['Ensolarado','Nublado','Nebuloso','Ventoso','Tempestuoso','Tempestades de areia'])

# Filtrando o DataFrame
linhas_filtradas = df['Densidade de tráfego'].isin( filtro_de_trafego )
df = df.loc[ linhas_filtradas, : ]

linhas_filtradas = df['Tipo de área'].isin( filtro_de_area )
df = df.loc[ linhas_filtradas, : ]

linhas_filtradas = df['Condição climática'].isin( filtro_de_clima )
df = df.loc[ linhas_filtradas, : ]

################################################################
# Botão de Download
################################################################

url = "https://raw.githubusercontent.com/CassioCandidoRibeiro/curry_company/main/curry.csv"
arquivo = fr.download_csv(url)
st.sidebar.download_button(
    label="Download do arquivo (.csv) utlizado",
    data=arquivo,
    file_name="curry.csv",
    mime="text/csv"
)

################################################
# PÁGINA
################################################
# 1. Empresa
# 2. Entregadores
# 3. Restaurantes
################################################

# Título
st.markdown('# Dashboard de Análise de Dados')
   
#Criando as 3 abas 
tab1, tab2, tab3 = st.tabs([
    '**1. Empresa**',
    '**2. Entregadores**',
    '**3. Restaurantes**'
])

#######################################
# 1. Empresa
#######################################
# 1. Quantidade de pedidos por dia.
# 2. Quantidade de pedidos por semana.
# 3. Distribuição dos pedidos por tipo de área.
# 4. Distribuição dos pedidos por densidade de tráfego.
# 5. Comparação do volume de pedidos por tipo de área e densidade de tráfego.
# 6. A quantidade de pedidos por entregador por semana.
# 7. A localização central de cada tipo de área por densidade de tráfego.
#######################################
with tab1:
    opcao = st.selectbox(
        'Escolha o que deseja ver:',(
            '1. Quantidade de pedidos por dia.',
            '2. Quantidade de pedidos por semana.',
            '3. Distribuição dos pedidos por tipo de área.',
            '4. Distribuição dos pedidos por densidade de tráfego.',
            '5. Comparação do volume de pedidos por tipo de área e densidade de tráfego.',
            '6. A quantidade de pedidos por entregador por semana.',
            '7. A localização central de cada tipo de área por densidade de tráfego.'))
    
    if opcao == '1. Quantidade de pedidos por dia.':
        st.plotly_chart( fr.pedidos_por_dia(df), ue_container_width=True)

    elif opcao == '2. Quantidade de pedidos por semana.':
        st.plotly_chart( fr.pedidos_por_semana(df), ue_container_width=True)

    elif opcao == '3. Distribuição dos pedidos por tipo de área.':
        st.plotly_chart( fr.pedidos_por_tipo_de_area(df), ue_container_width=True) 

    elif opcao == '4. Distribuição dos pedidos por densidade de tráfego.':
        st.plotly_chart( fr.pedidos_por_tipo_de_trafego(df), ue_container_width=True)    

    elif opcao == '5. Comparação do volume de pedidos por tipo de área e densidade de tráfego.':
        st.plotly_chart( fr.pedidos_por_tipo_de_area_e_tipo_de_trafego(df), ue_container_width=True)

    elif opcao == '6. A quantidade de pedidos por entregador por semana.':
        st.plotly_chart( fr.pedidos_por_entregador_por_semana(df), ue_container_width=True)

    elif opcao == '7. A localização central de cada tipo de área por densidade de tráfego.':
        folium_static( fr.localizacao_central_por_area_e_trafego(df) )

#######################################
# 2. Entregador
#######################################
# 1. A quantidade de entregadores por idade.
# 2. A quantidade de veículos em cada condição.
# 3. A avaliação médida por entregador.
# 4. A avaliação média e o desvio padrão por densidade de tráfego.
# 5. A avaliação média e o desvio padrão por condições climáticas.
# 6. Os 10 entregadores mais rápidos por tipo de área.
# 7. Os 10 entregadores mais lentos por tipo de área.
# 8. Tempo médio das entregas por densidade de tráfego.
# 9. Tempo médio das entregas por tipo de área.
# 10. Tempo médio de entrega por tipo de veículo.
# 11. Tempo médio de entrega por condição do veículo.
# 12. Tempo médio de entrega por idade do entregador.
# 13. Tempo médio de entrega por entregas multiplas.
# 14. Tempo médio de entrega por avaliação dos entregadores.
#######################################
with tab2:
    opcao = st.selectbox(
        'Escolha o que deseja ver:',(
            '1. A quantidade de entregadores por idade.',
            '2. A quantidade de veículos em cada condição.',
            '3. A avaliação médida por entregador.',
            '4. A avaliação média e o desvio padrão por densidade de tráfego.',
            '5. A avaliação média e o desvio padrão por condições climáticas.',
            '6. Os 10 entregadores mais rápidos por tipo de área.',
            '7. Os 10 entregadores mais lentos por tipo de área.',
            '8. Tempo médio das entregas por densidade de tráfego.',
            '9. Tempo médio das entregas por tipo de área.',
            '10. Tempo médio de entrega por tipo de veículo.',
            '11. Tempo médio de entrega por condição do veículo.',
            '12. Tempo médio de entrega por idade do entregador.',
            '13. Tempo médio de entrega por entregas multiplas.',
            '14. Tempo médio de entrega por avaliação dos entregadores.'))
    
    if opcao == '1. A quantidade de entregadores por idade.':
            st.plotly_chart( fr.quantidade_de_entregadores_por_idade(df), ue_container_width=True)

    elif opcao == '2. A quantidade de veículos em cada condição.':
        st.plotly_chart( fr.condicao_veiculos(df), ue_container_width=True)

    elif opcao == '3. A avaliação médida por entregador.':
        st.plotly_chart( fr.avaliacao_media_por_entregador(df), ue_container_width=True)

    elif opcao == '4. A avaliação média e o desvio padrão por densidade de tráfego.':
        st.table( fr.avaliacao_media_e_desvio_padrao_por_tipo_de_trafego(df) ) 

    elif opcao == '5. A avaliação média e o desvio padrão por condições climáticas.':
        st.table( fr.avaliacao_media_e_desvio_padrao_por_condicao_climatica(df))    

    elif opcao == '6. Os 10 entregadores mais rápidos por tipo de área.':
        col1, col2, col3 = st.columns(3, gap='small')
        with col1:
            st.table( fr.top10_entregadores_mais_rapidos_urbana(df).rename(columns={'ID do entregador':'Urbana'}) )
        with col2:
            st.table( fr.top10_entregadores_mais_rapidos_semi_urbana(df).rename(columns={'ID do entregador':'Semi-urbana'}) )
        with col3:
            st.table( fr.top10_entregadores_mais_rapidos_metropolitana(df).rename(columns={'ID do entregador':'Metropolitana'}) )
        
    elif opcao == '7. Os 10 entregadores mais lentos por tipo de área.':
        col1, col2, col3 = st.columns(3, gap='small')
        with col1:
            st.table( fr.top10_entregadores_mais_lentos_urbana(df).rename(columns={'ID do entregador':'Urbana'}) )
        with col2:
            st.table( fr.top10_entregadores_mais_lentos_semi_urbana(df).rename(columns={'ID do entregador':'Semi-urbana'}) )
        with col3:
            st.table( fr.top10_entregadores_mais_lentos_metropolitana(df).rename(columns={'ID do entregador':'Metropolitana'}) )

    elif opcao == '8. Tempo médio das entregas por densidade de tráfego.':
        st.plotly_chart( fr.tempo_medio_por_tipo_de_trafego(df), ue_container_width=True)

    elif opcao == '9. Tempo médio das entregas por tipo de área.':
        st.plotly_chart( fr.tempo_medio_das_entregas_por_tipo_de_area(df), ue_container_width=True) 

    elif opcao == '10. Tempo médio de entrega por tipo de veículo.':
        st.plotly_chart( fr.tempo_medio_de_entrega_por_tipo_de_veiculo(df), ue_container_width=True)    

    elif opcao == '11. Tempo médio de entrega por condição do veículo.':
        st.plotly_chart( fr.tempo_medio_de_entrega_por_condicao_do_veiculo(df), ue_container_width=True)

    elif opcao == '12. Tempo médio de entrega por idade do entregador.':
        st.plotly_chart( fr.tempo_medio_de_entrega_por_idade_do_entregador(df), ue_container_width=True)

    elif opcao == '13. Tempo médio de entrega por entregas multiplas.':
        st.plotly_chart( fr.tempo_medio_de_entrega_por_entregas_multiplas(df), ue_container_width=True)

    elif opcao == '14. Tempo médio de entrega por avaliação dos entregadores.':
        st.plotly_chart( fr.tempo_medio_de_entrega_por_avaliacao_dos_entregadores(df), ue_container_width=True) 

#######################################
# 3. Restaurante
#######################################
# 1. A quantidade de entregadores únicos.
# 2. A distância média dos resturantes e dos locais de entrega.
# 3. O tempo médio e o desvio padrão de entrega por tipo de área.
# 4. O tempo médio e o desvio padrão de entrega por tipo de área e tipo de pedido.
# 5. O tempo médio e o desvio padrão de entrega por tipo de área e densidade de tráfego.
# 6. O tempo médio de entrega durantes os Festivais.
#######################################
with tab3:
    opcao= st.selectbox(
        'Escolha o que deseja ver:',(
            '1. A quantidade de entregadores únicos.',
            '2. A distância média dos resturantes e dos locais de entrega.',
            '3. O tempo médio e o desvio padrão de entrega por tipo de área.',
            '4. O tempo médio e o desvio padrão de entrega por tipo de pedido.',
            '5. O tempo médio e o desvio padrão de entrega por densidade de tráfego.',
            '6. O tempo médio de entrega durantes os Festivais.'))
    
    if opcao == '1. A quantidade de entregadores únicos.':
        st.header( fr.quantidade_de_entregadores_unicos(df) )

    elif opcao == '2. A distância média dos resturantes e dos locais de entrega.':
        st.table( fr.distancia_media_dos_restaurantes_e_dos_locais_de_entrega(df) )    

    elif opcao == '3. O tempo médio e o desvio padrão de entrega por tipo de área.':
        st.table( fr.tempo_medio_e_desvio_padrao_por_tipo_de_area(df))        

    elif opcao == '4. O tempo médio e o desvio padrão de entrega por tipo de pedido.':
        st.table( fr.tempo_medio_e_desvio_padrao_por_tipo_de_pedido(df))

    elif opcao == '5. O tempo médio e o desvio padrão de entrega por densidade de tráfego.':
        st.table( fr.tempo_medio_e_desvio_padrao_por_tipo_de_trafego(df))    

    elif opcao == '6. O tempo médio de entrega durantes os Festivais.':
        st.table( fr.tempo_medio_e_desvio_padrao_durante_o_festival(df))   


################################################
# Rodapé
st.markdown('---')
st.markdown('Desenvolvido por [**Cássio Cândido Ribeiro**](https://www.linkedin.com/in/cassiocandidoribeiro), em parceria com a **Comunidade DS**.')