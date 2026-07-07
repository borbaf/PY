LAB365 / SENAI-SC — SCTEC Ciclo 2

ANÁLISE EXPLORATÓRIA DE DADOS — SAMPLE SUPERSTORE

Documentação Técnica e Relatório de Insights Logísticos

07 de julho de 2026

---

## Análise Exploratória de Dados — Sample Superstore
### Desafio Extra — Introdução ao Data Science (IP 20h A) — SCTEC Ciclo 2

### 1. Identificação do Projeto
- **Projeto:** Análise Exploratória de Dados (AED) — Sample Superstore Dataset
- **Autor:** Filippe Borba — Engenheiro e Consultor de Transformação Logística
- **Curso:** Introdução ao Data Science (IP 20h A)
- **Instituição:** LAB365 / SENAI-SC
- **Programa:** SCTEC — Carreira Tech, Ciclo 2
- **Data:** 07 de julho de 2026
- **Linguagem:** Python 3
- **Bibliotecas:** pandas, numpy, matplotlib, seaborn

### 2. Descrição das Etapas de Desenvolvimento

**Etapa 1 — Importação e Compreensão dos Dados:**
O dataset foi carregado com encoding `cp1252`. A exploração inicial revelou 9.994 registros e 21 colunas, incluindo informações de pedidos, clientes, produtos, vendas, descontos e lucros. Foram utilizados os métodos `info()`, `describe()`, `head()` e `dtypes` para compreender a estrutura e os tipos de dados.

**Etapa 2 — Tratamento e Preparação dos Dados:**
- Padronização dos nomes das colunas para lowercase com underscores (ex: "Order Date" → `order_date`)
- Verificação de valores nulos: nenhum valor nulo encontrado
- Verificação de duplicatas: nenhuma duplicata encontrada
- Conversão das colunas `order_date` e `ship_date` para o tipo datetime
- Garantia de que as colunas numéricas (sales, quantity, discount, profit) estivessem com os tipos corretos
- Identificação e tratamento de outliers usando o método IQR (Interquartile Range) nas colunas "sales" e "profit":
  - Sales: Q1=17.28, Q3=209.94, IQR=192.66 → 1.167 outliers removidos
  - Profit: Q1=1.70, Q3=21.34, IQR=19.63 → 1.435 outliers removidos
  - Dataset final após tratamento: 7.392 registros (de 9.994 originais)

**Etapa 3 — Análise Exploratória:**
Foram realizadas as seguintes análises:
- Resumo geral: Total de vendas `$460.629,52`, lucro total `$71.229,68`, 25.613 unidades vendidas
- GroupBy por Categoria: Office Supplies lidera com `$202.364` em vendas
- GroupBy por Segmento: Consumer representa `$245.715` em vendas (53% do total)
- GroupBy por Região: West domina com `$176.752` em vendas
- Análise Desconto vs Lucro: correlação de `-0,4774` (correlação negativa moderada)
- Tendência mensal: 48 períodos analisados, com picos em setembro a dezembro
- Top 10 produtos por vendas e por lucro
- Análise por sub-categoria (17 sub-categorias)
- Matriz de correlação entre variáveis numéricas

**Etapa 4 — Visualizações Gráficas (Etapa Comercial):**
9 gráficos foram gerados e salvos em PNG na pasta "graficos":
1. Vendas por Categoria (barras)
2. Lucro por Categoria (barras)
3. Vendas por Segmento (pizza)
4. Vendas por Região (barras)
5. Desconto vs Lucro (dispersão)
6. Tendência Mensal de Vendas e Lucro (linha)
7. Top 10 Produtos por Vendas (barras horizontais)
8. Matriz de Correlação (heatmap)
9. Lucro por Sub-Categoria (barras coloridas por positivo/negativo)

**Etapa 5 — Análise Logística (Perspectiva de Otimização):**
Esta etapa adicional foi desenvolvida sob a ótica de otimização logística, aproveitando a experiência profissional do autor como Engenheiro de Transformação Logística. Foram realizadas 6 análises logísticas:

- **5.1. Lead Time de Entrega:** Cálculo do tempo entre pedido e envio (`delivery_lead_time = ship_date - order_date`). Estatísticas de média, mediana, mínimo, máximo e desvio padrão. Análise do lead time por modo de envio (Standard Class, Second Class, First Class, Same Day).
- **5.2. Eficiência por Modo de Envio:** Agrupamento por `ship_mode` com vendas totais, lucro total, quantidade, número de pedidos, margem de lucro (%) e margem média por pedido. Identificação do modo de envio mais lucrativo.
- **5.3. Lead Time por Região:** Cruzamento do tempo de entrega com as regiões (West, East, Central, South) para identificar gargalos logísticos geográficos. Identificação da região com maior e menor lead time médio.
- **5.4. Consolidação de Pedidos:** Contagem de itens por `order_id` para avaliar o nível de consolidação. Estatísticas de média, mediana, máximo e mínimo de itens por pedido. Top 10 pedidos com maior consolidação.
- **5.5. Giro de Estoque por Sub-Categoria:** Análise da quantidade média vendida por produto único em cada sub-categoria, identificando produtos fast-moving (alto giro) e slow-moving (baixo giro), fundamental para planejamento de estoque de segurança.
- **5.6. Cross-Analysis Margem por Ship Mode vs Região:** Tabela pivot cruzando modos de envio com regiões, calculando a margem de lucro média (%) para cada combinação. Identificação da melhor e pior combinação logística.

4 gráficos logísticos adicionais foram gerados:
10. Lead Time médio por Ship Mode (barras)
11. Lead Time médio por Região (barras)
12. Margem de Lucro (%) por Ship Mode (barras)
13. Heatmap: Margem de Lucro por Ship Mode vs Região (mapa de calor)

### 3. Principais Decisões Tomadas Durante o Tratamento dos Dados

1. **Escolha do encoding cp1252:** O dataset original utiliza codificação Windows, e o `cp1252` foi o que permitiu a leitura correta dos caracteres especiais sem erros.
2. **Padronização de colunas:** Decidiu-se padronizar todos os nomes para lowercase com underscores para facilitar o acesso via `df.nome_coluna` e evitar inconsistências.
3. **Tratamento de outliers com IQR:** O método IQR foi escolhido por ser robusto e amplamente utilizado em EDA. Os limites de `1.5×IQR` removeram registros extremos que poderiam distorcer médias e correlações. A remoção reduziu o dataset de 9.994 para 7.392 registros, mantendo 74% dos dados originais — uma taxa de retenção aceitável.
4. **Integridade dos Dados:** Não houve necessidade de imputação de valores nulos ou remoção de duplicatas, pois o dataset já estava limpo neste aspecto.
5. **Análise Temporal:** As datas foram convertidas para datetime para permitir análise temporal e extração de períodos mensais, bem como o cálculo do lead time de entrega na Etapa 5.
6. **Criação de colunas derivadas:** `delivery_lead_time` (diferença entre ship_date e order_date) e `profit_margin` (lucro/vendas × 100) foram adicionadas para viabilizar as análises logísticas.
7. **Diferencial Profissional:** A escolha de adicionar uma Etapa 5 com foco logístico reflete a bagagem profissional do autor, transformando uma EDA padrão em uma análise com aplicabilidade prática para gestão de cadeias de suprimentos.

### 4. Principais Insights Obtidos

**Insights Comerciais (Etapas 1-4):**

1. **Correlação negativa entre desconto e lucro (-0,4774):** Descontos acima de 30% geram consistentemente lucro negativo. A partir de 50% de desconto, o prejuízo é sistemático. Isso sugere que a política de descontos precisa ser revista — descontos agressivos não estão gerando volume compensatório.
2. **Office Supplies é a categoria mais rentável:** Representa a maior fatia de vendas (`$202.364`) e lucro (`$44.257`), com margem saudável. É o motor financeiro da operação.
3. **Concentração geográfica:** A região West responde por 38% das vendas (`$176.752`), seguida pela East (25%). Há oportunidade de expansão nas regiões Central e South, que juntas representam apenas 36%.
4. **Segmento Consumer domina:** 53% das vendas (`$245.715`), mas com ticket médio menor. O segmento Home Office, embora menor, pode representar uma oportunidade de crescimento com estratégias de upsell.
5. **Sazonalidade:** Os meses de setembro a dezembro concentram os maiores volumes de vendas, indicando sazonalidade clara. Do ponto de vista logístico, isso exige planejamento prévio de capacidade de armazenagem, transporte e atendimento para o pico do Q4.
6. **Sub-categoria Tables apresenta lucro marginal:** Apesar de vendas moderadas (`$14.007`), o lucro é de apenas `$183` — sinal de que a margem desta sub-categoria é criticamente baixa e pode necessitar de revisão de pricing ou eliminação do portfolio.
7. **Paper é a sub-categoria mais eficiente em lucro:** Com `$38.317` em vendas, gera `$16.149` em lucro (margem de 42%) — excelente desempenho que merece destaque no mix de produtos.

**Insights Logísticos (Etapa 5):**

8. **Lead Time de Entrega:** O cálculo do tempo entre pedido e envio permite identificar quais modos de envio cumprem os SLAs esperados. O modo Same Day apresenta o menor lead time, enquanto Standard Class naturalmente tem o maior tempo de processamento.
9. **Eficiência por Modo de Envio:** A análise de margem de lucro por modo de envio revela qual modal é mais rentável por pedido, permitindo decisões sobre priorização de modos de envio mais eficientes.
10. **Gargalos Logísticos por Região:** A identificação da região com maior lead time médio sinaliza onde investir em infraestrutura logística — seja em centros de distribuição mais próximos, otimização de rotas ou parceiros de transporte local.
11. **Consolidação de Pedidos:** A análise de itens por pedido revela oportunidades de otimização de frete. Pedidos com múltiplos itens podem ser consolidados para reduzir custos de transporte, especialmente em modos de envio mais caros.
12. **Giro de Estoque:** A classificação fast-moving vs slow-moving por sub-categoria fornece subsídio direto para políticas de estoque de segurança. Sub-categorias fast-moving exigem maior cobertura de estoque, enquanto slow-moving podem ter reposição apenas sob demanda.
13. **Cross-Analysis Ship Mode × Região:** A matriz de margem de lucro cruzando modo de envio e região identifica a combinação mais eficiente e a menos eficiente, permitindo direcionar investimentos logísticos onde o retorno é maior.

### 5. Guia Rápido de Execução

1. Certifique-se de ter Python 3.x instalado.
2. Instale as dependências: `pip install pandas numpy matplotlib seaborn`.
3. Coloque o arquivo `Sample - Superstore.csv` na mesma pasta do script `main.py`.
4. Execute o script: `python main.py`.
5. Os gráficos serão salvos automaticamente na pasta `graficos/` (13 arquivos PNG).
6. O resultado da análise será impresso no console, incluindo o resumo executivo de insights logísticos.

**Estrutura de arquivos do projeto:**
- `main.py` (código-fonte com 5 etapas de análise)
- `Sample - Superstore.csv` (dataset)
- `graficos/` (pasta com os 13 gráficos em PNG)
- `README.md` (esta documentação)

### 6. Considerações Finais

A análise exploratória revelou padrões importantes sobre o comportamento comercial da rede varejista, com destaque para a relação inversa entre descontos e rentabilidade, a concentração geográfica das vendas e a sazonalidade do Q4. A inclusão da Etapa 5 (Análise Logística) trouxe uma camada adicional de inteligência analítica, aproveitando a experiência profissional do autor em transformação logística para extrair insights operacionais acionáveis — como identificação de gargalos de entrega por região, eficiência comparativa entre modos de envio, oportunidades de consolidação de pedidos e classificação de giro de estoque. Esta abordagem demonstra como a EDA pode ir além da descrição comercial e gerar recomendações concretas para otimização da cadeia de suprimentos.
