# 1. Problema de negócio

A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas.

Através desse aplicativo, é possível realizar o pedido de uma refeição, em qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por um entregador também cadastrado no aplicativo da Cury Company.

A empresa realiza negócios entre restaurantes, entregadores e pessoas, e gera muitos dados sobre entregas, tipos de pedidos, condições climáticas, avaliação dos entregadores e etc. Apesar da entrega estar crescento, em termos de entregas, o CEO não tem visibilidade completa dos KPIs de crescimento da empresa.

Você foi contratado como um Cientista de Dados para criar soluções de dados para entrega, mas antes de treinar algoritmos, a necessidade da empresa é ter um os principais KPIs estratégicos organizados em uma única ferramenta, para que o CEO possa consultar e conseguir tomar decisões simples, porém importantes.

A Cury Company possui um modelo de negócio chamado Marketplace, que fazer o intermédio do negócio entre três clientes principais: restaurantes, entregadores e pessoas compradoras. 

Para acompanhar o crescimento dos negócios, o CEO gostaria de ver algumas métricas indicadoras da performance da empresa.

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam essas métricas da melhor forma possível para o CEO.

# 2. Premissas assumidas para a análise

1. A análise foi realizada com dados entre 11/02/2022 e 06/04/2022.
2. Marketplace foi o modelo de negócio assumido.
3. As 3 principais visões do negócio foram: de transação de pedidos, dos restaurante e dos entregadores.

# 3. Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio da empresa:

1. Visão do crescimento da empresa
2. Visão do crescimento dos restaurantes
3. Visão do crescimento dos entregadores

Cada visão é representada pelo seguinte conjunto de métricas.

## Do lado da empresa:

1. Quantidade de entregas realizadas por dia.
2. Quantidade de entregas realizados por semana.
3. Distribuição das entregas por tipo de área (urbana, semi-urbana, metropolitana).
4. Distribuição das entregas por densidade de tráfego (baixo,médio,alto,engarrafado).
5. Comparação do volume de entregas por tipo de área e densidade de tráfego.
6. A quantidade de entregas por entregador por semana.
7. A localização central de cada tipo de área por densidade de tráfego.

## Do lado do entregador:

1. A quantidade de entregadores e as idade deles.
2. A quantidade de veículos em cada condição.
3. A avaliação média de cada entregador.
4. A avaliação média e o desvio padrão por densidade de tráfego.
5. A avaliação média e o desvio padrão por condições climáticas.
6. Os 10 entregadores mais rápidos por tipo de área.
7. Os 10 entregadores mais lentos por tipo de área.
8. Tempo médio das entregas por densidade de tráfego.
9. Tempo médio das entregas por tipo de área.
10. Tempo médio de entrega por tipo de veículo.
11. Tempo médio de entrega por condição do veículo.
12. Tempo médio de entrega por idade do entregador.
13. Tempo médio de entrega por entregas multiplas.
14. Tempo médio de entrega por avaliação dos entregadores.

## Do lado do restaurantes:

1. A quantidade de entregadores únicos.
2. A distância média dos resturantes e dos locais de entrega.
3. O tempo médio e o desvio padrão de entrega por tipo de área.
4. O tempo médio e o desvio padrão de entrega por tipo de área e tipo de pedido.
5. O tempo médio e o desvio padrão de entrega por tipo de área e densidade de tráfego.
6. O tempo médio de entrega durantes os Festivais.

# 4. Top 5 insights

1. A sazonalidade da quantidade de pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em dia sequenciais.
2. A área metropolitana concentra a maior quantidade de entregas apesar do trânsito engarrafado.
3. Um terço dos veículos estão em situação ruim, são 25% mais lentos que a média dos demais.
4. Em média, os entregadores com mais de 30 anos são 26% mais lentos  
5. As melhores avaliações são para as entregas mais rápidas

# 5. O produto final do projeto

Dashboard online, hospedado em um Cloud e disponível para acesso em qualquer dispositivo conectado à internet.
Pode ser acessado através desse link: https://cassiocandidoribeiro-curry-company.streamlit.app/

# 6. Conclusão

O objetivo desse projeto era criar um conjunto de gráficos e/ou tabelas que exibisse essas métricas da melhor forma possível para o CEO.
Da visão da Empresa, podemos concluir que o número de pedidos cresceu mais entre a semana 06 e a semana 13 do ano de 2022.

# 7. Próximo passos
1. Reduzir o número de métricas.
2. Criar outros filtros.
3. Adicionar novas visões de negócio.
4. Melhorar a visualização.

