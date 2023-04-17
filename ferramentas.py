#######################################
# Biblioteca
#######################################

# Manipulação dos dados
import pandas as pd

# Gráficos
import plotly.express as px

# Mapa
import folium

# Calcular distancias de GPS
from geopy.distance import geodesic 

# Para botão de download
import requests

#######################################
# Funções de limpeza
#######################################

def limpeza_dos_dados(df):
  '''
  # 1. Renomear as colunas do DataFrame. 
  # 2. Retirar do DataFrame linhas que possuem alguma informação faltando/vazia/não preenchida.
  # 3. Tirar os espaços em branco que estão sobrando, e retirar um prefixo da coluna de condição climática.
  # 4. Converter o tipo primitivo de algumas colunas
  # 5. Remover o prefixos
  # 6. Traduzir os objetos de algumas colunas para o português.
  # 7. Ordena a Densidade de tráfego
  # 8. Ordena a Condição Climática
  # 9. Cria a coluna 'Distancia (km)' 
  '''

  # 1. Renomear as colunas do DataFrame.
  dicionario = {
      'ID':'ID da entrega',
      'Delivery_person_ID':'ID do entregador', 
      'Delivery_person_Age':'Idade do entregador',
      'Delivery_person_Ratings':'Avaliação do entregador', 
      'Restaurant_latitude':'Latitude do restaurante',
      'Restaurant_longitude':'Longitude do restaurante', 
      'Delivery_location_latitude':'Latitude da entrega',
      'Delivery_location_longitude':'Longitude da entrega', 
      'Order_Date':'Data do pedido', 
      'Time_Orderd':'Horário do pedido',
      'Time_Order_picked':'Horário da retirada', 
      'Weatherconditions':'Condição climática', 
      'Road_traffic_density':'Densidade de tráfego',
      'Vehicle_condition':'Condição do veículo', 
      'Type_of_order':'Tipo de pedido', 
      'Type_of_vehicle':'Tipo de veículo',
      'multiple_deliveries':'Entregas multiplas', 
      'Festival':'Festival', 
      'City':'Tipo de área', 
      'Time_taken(min)':'Tempo de entrega (min)'
  }
  df = df.rename(columns=dicionario)

  # 2. Retirar do DataFrame linhas que possuem alguma informação faltando/vazia/não preenchida.
  df = df.dropna()
  # Exclui as linhas vazias 
  colunas = df.columns
  for coluna in colunas:
    linhas = (df[coluna] != 'NaN') & (df[coluna] != 'NaN ')
    df = df.loc[linhas,:]

  # 3. Tirar os espaços em branco que estão sobrando, e retirar um prefixo da coluna de condição climática.
  # Remove linhas com alguma coluna vazia.
  df = df.dropna()
  # Remove espaço em branco no fim das strings 
  colunas_str = df.select_dtypes(include='object').columns
  colunas = colunas_str
  for coluna in colunas:
    df.loc[:,coluna] = df.loc[:,coluna].str.strip()

  # 4. Converter o tipo primitivo de algumas colunas
  # Converte para numeros inteiros
  df['Idade do entregador'] = df['Idade do entregador'].astype(int)
  df['Entregas multiplas'] = df['Entregas multiplas'].astype(int)
  # Converte para numeros decimais
  df['Avaliação do entregador'] = df['Avaliação do entregador'].astype(float)
  df['Latitude do restaurante'] = df['Latitude do restaurante'].astype(float)
  df['Longitude do restaurante'] = df['Longitude do restaurante'].astype(float)
  df['Latitude da entrega'] = df['Latitude da entrega'].astype(float)
  df['Longitude da entrega'] = df['Longitude da entrega'].astype(float)
  # Conversao de texto para data
  df['Data do pedido'] = pd.to_datetime( df['Data do pedido'], format='%d-%m-%Y')
  # Extrai a 'str' e deixa os números em formato 'int'
  df['Tempo de entrega (min)'] = df['Tempo de entrega (min)'].str.extract(r'(\d+)').astype(int)

  # 5. Remover o prefixos
  # Prefixo "conditions" da coluna de Condição climática
  df['Condição climática'] = df['Condição climática'].str.replace('conditions ', '')

  # 6. Traduzir os objetos de algumas colunas para o português.
  # Condição climática
  dicionario = {
      'Sunny': 'Ensolarado',
      'Stormy': 'Tempestuoso',
      'Sandstorms': 'Tempestades de areia',
      'Cloudy': 'Nublado',
      'Fog': 'Nebuloso',
      'Windy': 'Ventoso'
      }
  df['Condição climática'] = df['Condição climática'].map(dicionario)
  
  # Tipo de área
  dicionario = {
      'Urban': 'Urbana',
      'Metropolitian': 'Metropolitana',
      'Semi-Urban': 'Semi-urbana'
      }
  df['Tipo de área'] = df['Tipo de área'].map(dicionario)

  # Densidade de tráfego
  dicionario = {
      'High': 'Alto',
      'Jam': 'Engarrafado',
      'Low': 'Baixo',
      'Medium': 'Médio'
      }
  df['Densidade de tráfego'] = df['Densidade de tráfego'].map(dicionario)

  # Festival
  dicionario = {
      'Yes': 'Sim',
      'No': 'Não'
      }
  df['Festival'] = df['Festival'].map(dicionario)

  # Tipo de veículo
  dicionario = {
    'motorcycle': 'Motocicleta',
    'scooter': 'Scooter',
    'electric_scooter': 'Scooter Elétrica'
      }
  df['Tipo de veículo'] = df['Tipo de veículo'].map(dicionario)

  # Tipo de pedido
  dicionario = {
      'Snack': 'Lanche',
      'Drinks': 'Bebidas',
      'Buffet': 'Buffet',
      'Meal': 'Refeição'
      }
  df['Tipo de pedido'] = df['Tipo de pedido'].map(dicionario)

  # Condição do veículo
  dicionario = {
      0:'Ruim',
      1:'Normal',
      2:'Boa'
      }
  df['Condição do veículo'] = df['Condição do veículo'].map(dicionario)

  # 7. Ordena a Densidade de tráfego
  ordem_densidade = ['Baixo', 'Médio', 'Alto', 'Engarrafado']
  df['Densidade de tráfego'] = pd.Categorical(df['Densidade de tráfego'], categories=ordem_densidade, ordered=True)
  
  # 8. Ordena a Condição Climática
  ordem_condicao_climatica = ['Ensolarado', 'Nublado', 'Nebuloso', 'Ventoso','Tempestuoso','Tempestades de areia']
  df['Condição climática'] = pd.Categorical(df['Condição climática'], categories=ordem_condicao_climatica, ordered=True)

  # 9. Cria a coluna 'Distancia (km)'
  def calcular_distancia(lat1, long1, lat2, long2):
      coords_1 = (lat1, long1)
      coords_2 = (lat2, long2)
      return geodesic(coords_1, coords_2).km
  df['Distância (km)'] = df.apply(lambda row: calcular_distancia(row['Latitude do restaurante'], row['Longitude do restaurante'], row['Latitude da entrega'], row['Longitude da entrega']), axis=1)
  
  return df

#######################################
# Funções de análise
#######################################
# Empresa / Entregador / Restaurante
#######################################

#######################################
# Empresa
#######################################
# 1. Quantidade de pedidos por dia.
# 2. Quantidade de pedidos por semana.
# 3. Distribuição dos pedidos por densidade de tráfego.
# 4. Distribuição dos pedidos por densidade de tráfego.
# 5. Comparação do volume de pedidos por tipo de área e densidade de tráfego.
# 6. A quantidade de pedidos por entregador por semana.
# 7. A localização central de cada tipo de área por densidade de tráfego.
#######################################

# 1. Quantidade de pedidos por dia.
def pedidos_por_dia(df):
  df_aux = df.loc[:, ['ID da entrega', 'Data do pedido'] ].groupby('Data do pedido').count().reset_index()
  # Criando gráfico de barras
  fig = px.bar(
    df_aux,
    x='Data do pedido' , 
    y='ID da entrega', 
    title='Quantidade de pedidos por dia.')
  return fig

# 2. Quantidade de pedidos por semana
def pedidos_por_semana(df):
    # Criando uma nova coluna, que indica a semana do ano
    df['Semana'] = df['Data do pedido'].dt.strftime( '%U' )
    # Selecionando a coluna ID e agrupando pela semana do ano
    df_aux = df.loc[:, ['ID da entrega','Semana'] ].groupby('Semana').count().reset_index()
    # Criando gráfico de linha
    fig = px.line(df_aux, x='Semana',y='ID da entrega' , title='Quantidade de pedidos por semana')
    return fig

# 3. Distribuição dos pedidos por tipo de área.
def pedidos_por_tipo_de_area(df):
  df_aux = df.loc[:, ['ID da entrega', 'Tipo de área'] ].groupby('Tipo de área').count().reset_index()
  # Criando o gráfico de torta
  fig = px.pie(
    df_aux,values='ID da entrega',
    names='Tipo de área', 
    title='Distribuição dos pedidos por tipo de área.', 
    color_discrete_sequence=['green','red','blue'], 
    labels={'ID da entrega':'Quantidade de pedidos'})
  return fig

# 4. Distribuição dos pedidos por densidade de tráfego.
def pedidos_por_tipo_de_trafego(df):
  df_aux = df.loc[:, ['ID da entrega', 'Densidade de tráfego'] ].groupby('Densidade de tráfego').count().reset_index()
  # Criando o gráfico de torta
  fig = px.pie(
    df_aux,values='ID da entrega',
    names='Densidade de tráfego', 
    title='Distribuição dos pedidos por densidade de tráfego.', 
    color_discrete_sequence=['green','red','blue','orange'], 
    labels={'ID da entrega':'Quantidade de pedidos'})
  return fig

# 5. Comparação do volume de pedidos por tipo de área e de tráfego.
def pedidos_por_tipo_de_area_e_tipo_de_trafego(df):
  df_aux = df.groupby(['Densidade de tráfego','Tipo de área'])['ID da entrega'].count().reset_index()
  # Criando o gráfico
  fig = px.bar(
    df_aux,
    x='Tipo de área' , 
    y='ID da entrega',
    color='Densidade de tráfego',
    color_discrete_sequence=['green','blue','orange','red'],
    title='Comparação do volume de pedidos por tipo de área e densidade de tráfego.',
    barmode='group',
    labels={'ID da entrega':'Quantidade de pedidos'})
  return fig

# 6. A quantidade de pedidos por entregador por semana.
def pedidos_por_entregador_por_semana(df):
  # Criando uma nova coluna, que indica a semana do ano
  df['Semana'] = df['Data do pedido'].dt.strftime( '%U' )
  # Agrupando os dados por semana e contando o número de entregas por semana
  A = df.loc[:,['ID da entrega','Semana']].groupby('Semana').count().reset_index()
  # Agrupando os dados por semana e contando o número de entregadores únicos por semana
  B = df.loc[:,['ID do entregador','Semana']].groupby('Semana').nunique().reset_index()
  # Fazendo um join entre os dataframes A e B, com base na coluna 'Semana'
  df_aux = pd.merge(A,B, how = 'inner')
  # Criando uma nova coluna 'Pedido por entregador', que indica a média de entregas por entregador em cada semana
  df_aux['Pedido por entregador'] = df_aux['ID da entrega'] / df_aux['ID do entregador']
  # Criando o gráfico
  fig = px.line(
    df_aux, 
    x='Semana', 
    y='Pedido por entregador', 
    title='A quantidade de pedidos por entregador por semana.' )
  return fig

# 7. A localização central de cada tipo de área por densidade de tráfego.
def localizacao_central_por_area_e_trafego(df):
  df_aux = df.loc[:,['Tipo de área', 'Densidade de tráfego', 'Latitude da entrega', 'Longitude da entrega']].groupby(['Tipo de área','Densidade de tráfego']).median().reset_index()
  df_aux = df_aux.dropna()

  # Definindo o mapa
  mapa = folium.Map(
      location=([df_aux.loc[1,'Latitude da entrega'], df_aux.loc[1,'Longitude da entrega']]),
      zoom_start=7,
      control_scale=True,
      responsive=True,
      max_bounds=True
      )
    
  for index, coluna in df_aux.iterrows():
    # Informações do popup
    area= coluna['Tipo de área']
    trafego= coluna['Densidade de tráfego']

    # Texto do popup dos marcadores
    html = "<p>Tipo de área: {}</br>"
    html += "Densidade de tráfego: {}"
    html = html.format(area, trafego)
    
    # Definindo o popup
    popup = folium.Popup(folium.Html(html, script=True),max_width=500)
    folium.Marker(
      location=([coluna['Latitude da entrega'], coluna['Longitude da entrega']]),
      popup= popup,
      icon= folium.Icon(
        icon='glyphicon glyphicon-home',
        color= 'blue',
        icon_color= 'white',
        prefix= 'glyphicon'
      )
    ).add_to(mapa)
  return mapa

#######################################
# Entregador
#######################################
# 1. A quantidade de entregadores por idade.
# 2. A quantidade de veículos em cada condição.
# 3. A avaliação média por entregador.
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
# 15. Tempo médio de entrega por condição climática.
#######################################

# 1. A quantidade de entregadores por idade.
def quantidade_de_entregadores_por_idade(df):
  df_aux = df.loc[:,['ID do entregador','Idade do entregador']].groupby('Idade do entregador').nunique().reset_index()
  fig = px.bar(
    df_aux,
    x='Idade do entregador',
    y='ID do entregador',
    title='A quantidade de entregadores por idade.',
    labels={'ID do entregador':'Quantidade de entregadores'}
  )
  return fig

# 2. A pior e a melhor condição de veículos.
def condicao_veiculos(df):
  df_aux = df.loc[:, ['ID do entregador', 'Condição do veículo'] ].groupby('Condição do veículo').nunique().reset_index()
  fig = px.pie(
    df_aux,
    values='ID do entregador',
    names='Condição do veículo', 
    title='A quantidade de veículos em cada condição.', 
    color_discrete_sequence=['blue','red','green'], 
    labels={'ID do entregador':'Quantidade de entregadores'}
  )
  return fig

# 3. Quantidade de entregadores por avaliação.
def avaliacao_media_por_entregador(df):
  df_aux = df.loc[:,['ID do entregador','Avaliação do entregador']].groupby('Avaliação do entregador').count().sort_values(by='Avaliação do entregador', ascending=False).reset_index()
  fig = px.bar(
    df_aux,
    x='ID do entregador',
    y='Avaliação do entregador',
    title='A avaliação média por entregador',
    labels={'ID do entregador':'Quantidade de entregadores'},
    orientation='h'
  )
  return fig

# 4. A avaliação média e o desvio padrão por densidade de tráfego.
def avaliacao_media_e_desvio_padrao_por_tipo_de_trafego(df):
  df_aux = df.loc[:,['Densidade de tráfego','Avaliação do entregador']].groupby('Densidade de tráfego').agg({'Avaliação do entregador':['mean','median','std']}).reset_index()
  df_aux.columns=['Densidade de tráfego','Avaliação média do entregador','Mediana','Desvio padrão (min)']
  df_aux.index +=1  
  return df_aux

# 5. A avaliação média e o desvio padrão por condições climáticas.
def avaliacao_media_e_desvio_padrao_por_condicao_climatica(df):
  df_aux = df.loc[:,['Condição climática','Avaliação do entregador']].groupby('Condição climática').agg({'Avaliação do entregador':['mean','median','std']}).reset_index()
  df_aux.columns=['Condição climática','Avaliação média do entregador','Mediana','Desvio padrão (min)']
  df_aux.index +=1
  return df_aux

# 6. Os 10 entregadores mais rápidos por tipo de área.
def top10_entregadores_mais_rapidos_urbana(df):
  df_aux = df[df['Tipo de área']=='Urbana']
  df_aux = df_aux.loc[:,['ID do entregador','Tempo de entrega (min)']].groupby(['ID do entregador']).mean().astype(int).sort_values(by='Tempo de entrega (min)',ascending=True).reset_index()
  df_aux.index += 1
  return df_aux.head(10)

def top10_entregadores_mais_rapidos_semi_urbana(df):
  df_aux = df[df['Tipo de área']=='Semi-urbana']
  df_aux = df_aux.loc[:,['ID do entregador','Tempo de entrega (min)']].groupby(['ID do entregador']).mean().astype(int).sort_values(by='Tempo de entrega (min)',ascending=True).reset_index()
  df_aux.index += 1
  return df_aux.head(10)
  
def top10_entregadores_mais_rapidos_metropolitana(df):
  df_aux = df[df['Tipo de área']=='Metropolitana']
  df_aux = df_aux.loc[:,['ID do entregador','Tempo de entrega (min)']].groupby(['ID do entregador']).mean().astype(int).sort_values(by='Tempo de entrega (min)',ascending=True).reset_index()
  df_aux.index += 1
  return df_aux.head(10)

# 7. Os 10 entregadores mais lentos por tipo de área.
def top10_entregadores_mais_lentos_urbana(df):
  df_aux = df[df['Tipo de área']=='Urbana']
  df_aux = df_aux.loc[:,['ID do entregador','Tempo de entrega (min)']].groupby(['ID do entregador']).mean().astype(int).sort_values(by='Tempo de entrega (min)',ascending=False).reset_index()
  df_aux.index += 1
  return df_aux.head(10)

def top10_entregadores_mais_lentos_semi_urbana(df):
  df_aux = df[df['Tipo de área']=='Semi-urbana']
  df_aux = df_aux.loc[:,['ID do entregador','Tempo de entrega (min)']].groupby(['ID do entregador']).mean().astype(int).sort_values(by='Tempo de entrega (min)',ascending=False).reset_index()
  df_aux.index += 1
  return df_aux.head(10)


def top10_entregadores_mais_lentos_metropolitana(df):
  df_aux = df[df['Tipo de área']=='Metropolitana']
  df_aux = df_aux.loc[:,['ID do entregador','Tempo de entrega (min)']].groupby(['ID do entregador']).mean().astype(int).sort_values(by='Tempo de entrega (min)',ascending=False).reset_index()
  df_aux.index += 1
  return df_aux.head(10)

# 8. Tempo médio das entregas por densidade de tráfego
def tempo_medio_por_tipo_de_trafego(df):
  df_aux = df.loc[:,['Densidade de tráfego','Tempo de entrega (min)']].groupby('Densidade de tráfego').mean().astype(int).sort_values(by='Tempo de entrega (min)',ascending=True).reset_index()
  fig = px.bar(
    df_aux,
    x='Densidade de tráfego',
    y='Tempo de entrega (min)',
    title='Tempo médio das entregas por densidade de tráfego',
  )
  return fig

# 9. Tempo médio das entregas por tipo de área
def tempo_medio_das_entregas_por_tipo_de_area(df):
  df_aux = df.loc[:,['Tipo de área','Tempo de entrega (min)']].groupby('Tipo de área').mean().astype(int).sort_values(by='Tempo de entrega (min)',ascending=True).reset_index()
  fig = px.bar(
    df_aux,
    x='Tipo de área',
    y='Tempo de entrega (min)',
    title='Tempo médio das entregas por tipo de área',
  )
  return fig

# 10. Tempo médio de entrega por tipo de veículo
def tempo_medio_de_entrega_por_tipo_de_veiculo(df):
  df_aux = df.loc[:,['Tipo de veículo','Tempo de entrega (min)']].groupby('Tipo de veículo').mean().astype(int).reset_index()
  fig = px.bar(
    df_aux,
    x='Tipo de veículo',
    y='Tempo de entrega (min)',
    title='Tempo médio das entregas por tipo de veículo',
  )
  return fig

# 11. Tempo médio de entrega por condição do veículo
def tempo_medio_de_entrega_por_condicao_do_veiculo(df):
  df_aux = df.loc[:,['Condição do veículo','Tempo de entrega (min)']].groupby('Condição do veículo').mean().astype(int).reset_index()
  fig = px.bar(
    df_aux,
    x='Condição do veículo',
    y='Tempo de entrega (min)',
    title='Tempo médio das entregas por tipo condição do veículo',
  )
  return fig

# 12. Tempo médio de entrega por idade do entregador
def tempo_medio_de_entrega_por_idade_do_entregador(df):
  df_aux = df.loc[:,['Idade do entregador','Tempo de entrega (min)']].groupby('Idade do entregador').mean().astype(int).reset_index()
  fig = px.bar(
    df_aux,
    x='Idade do entregador',
    y='Tempo de entrega (min)',
    title='Tempo médio das entregas por tipo idade do entregador',
  )
  return fig

# 13. Tempo médio de entrega por entregas multiplas.
def tempo_medio_de_entrega_por_entregas_multiplas(df):
  df_aux = df.loc[:,['Entregas multiplas','Tempo de entrega (min)']].groupby('Entregas multiplas').mean().astype(int).sort_values(by='Tempo de entrega (min)',ascending=True).reset_index()
  fig = px.bar(
    df_aux,
    x='Entregas multiplas',
    y='Tempo de entrega (min)',
    title='Tempo médio das entregas por entregas multiplas',
  )
  return fig

# 14. Tempo médio de entrega por avaliação dos entregadores.
def tempo_medio_de_entrega_por_avaliacao_dos_entregadores(df):
  df_aux = df.loc[:,['Avaliação do entregador','Tempo de entrega (min)']].groupby('Avaliação do entregador').mean().astype(int).reset_index()
  fig = px.bar(
    df_aux,
    x='Avaliação do entregador',
    y='Tempo de entrega (min)',
    title='Tempo médio das entregas por avaliação dos entregadores',
  )
  return fig

# 15. Tempo médio de entrega por condição climática.
def tempo_medio_de_entrega_por_condicao_climatica(df):
  df_aux = df.loc[:,['Condição climática','Tempo de entrega (min)']].groupby('Condição climática').mean().astype(int).sort_values(by='Tempo de entrega (min)',ascending=True).reset_index()
  fig = px.bar(
    df_aux,
    x='Condição climática',
    y='Tempo de entrega (min)',
    title='Tempo médio das entregas por Condição climática',
  )
  return fig


#######################################
# Restaurante
#######################################
# 1. A quantidade de entregadores únicos.
# 2. A distância média dos resturantes e dos locais de entrega.
# 3. O tempo médio e o desvio padrão de entrega por tipo de área.
# 4. O tempo médio e o desvio padrão de entrega por tipo de área e tipo de pedido.
# 5. O tempo médio e o desvio padrão de entrega por tipo de área e densidade de tráfego.
# 6. O tempo médio de entrega durantes os Festivais.
# 7. O tempo médio e o desvio padrão de entrega por condições climáticas.
#######################################

# 1. A quantidade de entregadores únicos.
def quantidade_de_entregadores_unicos(df):
  return df['ID do entregador'].nunique()

# 2. A distância média dos resturantes e dos locais de entrega.
def distancia_media_dos_restaurantes_e_dos_locais_de_entrega(df):
    df_aux = df['Distância (km)'].agg(['mean', 'median', 'std']).round(3)
    df_aux = df_aux.rename(index={'mean': 'Média', 'median': 'Mediana', 'std': 'Desvio Padrão'}).reset_index()
    df_aux = df_aux.rename(columns={'index': 'Estatística'})
    df_aux.index += 1
    return df_aux

# 3. O tempo médio e o desvio padrão de entrega por tipo de área.
def tempo_medio_e_desvio_padrao_por_tipo_de_area(df):
  df_aux = df.loc[:,['Tempo de entrega (min)','Tipo de área']].groupby('Tipo de área').agg({'Tempo de entrega (min)':['mean','mean','std']}).round(3).astype(int).reset_index()
  df_aux.columns=['Tipo de área','Tempo médio de entrega (min)','Mediana','Desvio padrão']
  df_aux.index += 1
  return df_aux

# 4. O tempo médio e o desvio padrão de entrega por tipo de pedido.
def tempo_medio_e_desvio_padrao_por_tipo_de_pedido(df):
  df_aux = df.loc[:,['Tempo de entrega (min)','Tipo de pedido']].groupby('Tipo de pedido').agg({'Tempo de entrega (min)':['mean','mean','std']}).round(3).astype(int).reset_index()
  df_aux.columns=['Tipo de pedido','Tempo médio de entrega (min)','Mediana','Desvio padrão']
  df_aux.index += 1
  return df_aux

# 5. O tempo médio e o desvio padrão de entrega por densidade de tráfego.
def tempo_medio_e_desvio_padrao_por_tipo_de_trafego(df):
  df_aux = df.loc[:,['Tempo de entrega (min)','Densidade de tráfego']].groupby('Densidade de tráfego').agg({'Tempo de entrega (min)':['mean','median','std']}).round(3).astype(int).reset_index()
  df_aux.columns=['Densidade de tráfego','Tempo médio de entrega (min)','Mediana','Desvio padrão']
  df_aux.index += 1
  return df_aux

# 6. O tempo médio e desvio padrão de entrega durantes os Festivais.
def tempo_medio_e_desvio_padrao_durante_o_festival(df):
  df_aux = df.loc[:,['Tempo de entrega (min)','Festival']].groupby('Festival').agg({'Tempo de entrega (min)':['mean','median','std']}).round(3).astype(int).reset_index()
  df_aux.columns=['Festival','Tempo médio de entrega (min)','Mediana','Desvio padrão']
  df_aux.index += 1
  return df_aux

# 7. O tempo médio e o desvio padrão de entrega por condições climáticas.
def tempo_medio_e_desvio_padrao_por_condicao_climatica(df):
  df_aux = df.loc[:,['Tempo de entrega (min)','Condição climática']].groupby('Condição climática').agg({'Tempo de entrega (min)':['mean','median','std']}).round(3).astype(int).reset_index()
  df_aux.columns=['Condição climática','Tempo médio de entrega (min)','Mediana','Desvio padrão']
  df_aux.index += 1
  return df_aux

################################################################
# Botão de Download
################################################################

# Função para fazer a requisição e retornar o conteúdo do arquivo
def download_csv(url):
  response = requests.get(url)
  content = response.content.decode("utf-8")
  return content

  