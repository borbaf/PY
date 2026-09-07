import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração de estilo dos gráficos
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# ---------------------------------------------------------------------
# CONFIGURAÇÃO DE CAMINHOS (robustez no tratamento de arquivos)
# ---------------------------------------------------------------------
# Diretório base do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho do arquivo CSV (mesma pasta do script)
CSV_PATH = os.path.join(BASE_DIR, "Sample - Superstore.csv")

# Pasta onde os gráficos serão salvos
GRAFICOS_DIR = os.path.join(BASE_DIR, "graficos")

# Lista para armazenar os arquivos gerados
arquivos_gerados = []


def criar_pasta_graficos():
    """Cria a pasta 'graficos' caso ela não exista."""
    if not os.path.exists(GRAFICOS_DIR):
        os.makedirs(GRAFICOS_DIR)
        print("[INFO] Pasta 'graficos' criada com sucesso.")
    else:
        print("[INFO] Pasta 'graficos' já existe.")


def imprimir_separador(titulo):
    """Imprime um separador formatado para cada etapa da análise."""
    print("\n" + "=" * 70)
    print(f"  {titulo}")
    print("=" * 70 + "\n")


def salvar_grafico(fig, nome_arquivo):
    """Salva o gráfico na pasta 'graficos' e fecha a figura para liberar memória."""
    caminho_completo = os.path.join(GRAFICOS_DIR, nome_arquivo)
    plt.tight_layout()
    fig.savefig(caminho_completo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    arquivos_gerados.append(nome_arquivo)
    print(f"[GRÁFICO SALVO] {nome_arquivo}")


# =====================================================================
# ETAPA 1: IMPORTAÇÃO E COMPREENSÃO DOS DADOS
# =====================================================================
def etapa1_importacao_compreensao():
    """Carrega o dataset e faz a exploração inicial da estrutura."""
    imprimir_separador("ETAPA 1: IMPORTAÇÃO E COMPREENSÃO DOS DADOS")

    # Verifica se o arquivo existe antes de tentar carregar
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"Arquivo não encontrado: {CSV_PATH}\n"
            "Certifique-se de que 'Sample - Superstore.csv' está na mesma pasta do script."
        )

    # Carregamento do CSV com encoding cp1252 para evitar problemas com caracteres especiais
    df = pd.read_csv(CSV_PATH, encoding="cp1252")
    print("[INFO] Dataset carregado com sucesso!\n")

    # Exibindo o formato do dataset (linhas, colunas)
    print(f"Formato do dataset (linhas, colunas): {df.shape}")

    # Informações gerais sobre o dataset
    print("\n--- Informações gerais do DataFrame ---")
    print(df.info())

    # Exibindo as primeiras linhas
    print("\n--- Primeiras 5 linhas do dataset ---")
    print(df.head())

    # Tipos de dados das colunas
    print("\n--- Tipos de dados das colunas ---")
    print(df.dtypes)

    # Estatísticas descritivas iniciais
    print("\n--- Estatísticas descritivas (numéricas) ---")
    print(df.describe())

    # Estatísticas descritivas para colunas categóricas
    print("\n--- Estatísticas descritivas (categóricas) ---")
    print(df.describe(include="object"))

    # Lista de colunas disponíveis
    print("\n--- Colunas disponíveis no dataset ---")
    for col in df.columns:
        print(f"  - {col}")

    return df


# =====================================================================
# ETAPA 2: TRATAMENTO E PREPARAÇÃO DOS DADOS
# =====================================================================
def etapa2_tratamento_preparacao(df):
    """Realiza a limpeza e preparação dos dados."""
    imprimir_separador("ETAPA 2: TRATAMENTO E PREPARAÇÃO DOS DADOS")

    # 2.1 - Padronização dos nomes das colunas (lowercase + underscores)
    print("[PASSO] Padronizando nomes das colunas (lowercase, underscores)...")
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    print("Novos nomes das colunas:")
    for col in df.columns:
        print(f"  - {col}")

    # 2.2 - Verificação de valores nulos
    print("\n[PASSO] Verificando valores nulos...")
    valores_nulos = df.isnull().sum()
    print(valores_nulos)
    total_nulos = valores_nulos.sum()
    print(f"\nTotal de valores nulos no dataset: {total_nulos}")

    if total_nulos > 0:
        print("[INFO] Removendo linhas com valores nulos...")
        df = df.dropna()
        print(f"Dataset após remoção de nulos: {df.shape}")
    else:
        print("[INFO] Nenhum valor nulo encontrado!")

    # 2.3 - Verificação e remoção de duplicatas
    print("\n[PASSO] Verificando duplicatas...")
    duplicatas = df.duplicated().sum()
    print(f"Total de linhas duplicadas: {duplicatas}")

    if duplicatas > 0:
        print("[INFO] Removendo duplicatas...")
        df = df.drop_duplicates()
        print(f"Dataset após remoção de duplicatas: {df.shape}")
    else:
        print("[INFO] Nenhuma duplicata encontrada!")

    # 2.4 - Conversão de colunas de data para datetime
    print("\n[PASSO] Convertendo colunas de data para datetime...")
    colunas_data = ["order_date", "ship_date"]
    for col in colunas_data:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            print(f"  Coluna '{col}' convertida para datetime.")
        else:
            print(f"  [AVISO] Coluna '{col}' não encontrada no dataset.")

    # 2.5 - Garantir que colunas numéricas tenham o tipo correto
    print("\n[PASSO] Garantindo tipos numéricos corretos...")
    colunas_numericas = ["sales", "quantity", "discount", "profit"]
    for col in colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            print(f"  Coluna '{col}' -> tipo: {df[col].dtype}")
        else:
            print(f"  [AVISO] Coluna '{col}' não encontrada.")

    # 2.6 - Identificação e tratamento de outliers (IQR) em Sales e Profit
    print("\n[PASSO] Identificando e tratando outliers (método IQR)...")

    def tratar_outliers_iqr(dataframe, coluna):
        """Remove outliers de uma coluna usando o método IQR."""
        Q1 = dataframe[coluna].quantile(0.25)
        Q3 = dataframe[coluna].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        outliers = dataframe[(dataframe[coluna] < limite_inferior) | (dataframe[coluna] > limite_superior)]
        print(f"  Coluna '{coluna}':")
        print(f"    Q1 = {Q1:.2f} | Q3 = {Q3:.2f} | IQR = {IQR:.2f}")
        print(f"    Limite inferior = {limite_inferior:.2f} | Limite superior = {limite_superior:.2f}")
        print(f"    Outliers encontrados: {len(outliers)}")

        # Filtra mantendo apenas valores dentro dos limites
        dataframe = dataframe[(dataframe[coluna] >= limite_inferior) & (dataframe[coluna] <= limite_superior)]
        return dataframe

    print(f"\nFormato antes do tratamento de outliers: {df.shape}")
    df = tratar_outliers_iqr(df, "sales")
    df = tratar_outliers_iqr(df, "profit")
    print(f"\nFormato após tratamento de outliers: {df.shape}")

    # Exibindo o dataset tratado
    print("\n--- Primeiras linhas do dataset tratado ---")
    print(df.head())

    print("\n--- Informações do dataset tratado ---")
    print(df.info())

    return df


# =====================================================================
# ETAPA 3: ANÁLISE EXPLORATÓRIA
# =====================================================================
def etapa3_analise_exploratoria(df):
    """Realiza a análise exploratória dos dados."""
    imprimir_separador("ETAPA 3: ANÁLISE EXPLORATÓRIA")

    # 3.1 - Resumo geral: vendas, lucro e quantidade
    print("[ANÁLISE] Resumo geral de Vendas, Lucro e Quantidade:")
    print(f"  Total de Vendas (Sales):    ${df['sales'].sum():,.2f}")
    print(f"  Total de Lucro (Profit):    ${df['profit'].sum():,.2f}")
    print(f"  Total de Quantidade (Qty):  {df['quantity'].sum():,}")
    print(f"  Ticket médio de Vendas:     ${df['sales'].mean():,.2f}")
    print(f"  Lucro médio:                ${df['profit'].mean():,.2f}")

    # 3.2 - GroupBy: Vendas e Lucro por Categoria
    print("\n[ANÁLISE] Vendas e Lucro por Categoria:")
    categoria = df.groupby("category").agg({
        "sales": "sum",
        "profit": "sum",
        "quantity": "sum"
    }).sort_values(by="sales", ascending=False)
    print(categoria)

    # 3.3 - GroupBy: Vendas e Lucro por Segmento
    print("\n[ANÁLISE] Vendas e Lucro por Segmento:")
    segmento = df.groupby("segment").agg({
        "sales": "sum",
        "profit": "sum",
        "quantity": "sum"
    }).sort_values(by="sales", ascending=False)
    print(segmento)

    # 3.4 - GroupBy: Vendas e Lucro por Região
    print("\n[ANÁLISE] Vendas e Lucro por Região:")
    regiao = df.groupby("region").agg({
        "sales": "sum",
        "profit": "sum",
        "quantity": "sum"
    }).sort_values(by="sales", ascending=False)
    print(regiao)

    # 3.5 - Análise da relação entre Desconto e Lucro
    print("\n[ANÁLISE] Relação entre Desconto (Discount) e Lucro (Profit):")
    correlacao_discount_profit = df["discount"].corr(df["profit"])
    print(f"  Correlação entre Discount e Profit: {correlacao_discount_profit:.4f}")
    print("\n  Lucro médio por nível de desconto:")
    discount_profit = df.groupby("discount").agg({
        "profit": ["mean", "sum", "count"]
    }).round(2)
    print(discount_profit)

    # 3.6 - Série temporal: tendência mensal de vendas e lucro
    print("\n[ANÁLISE] Tendência mensal de Vendas e Lucro:")
    df_temporal = df.copy()
    df_temporal["ano_mes"] = df_temporal["order_date"].dt.to_period("M")
    mensal = df_temporal.groupby("ano_mes").agg({
        "sales": "sum",
        "profit": "sum"
    }).reset_index()
    mensal["ano_mes"] = mensal["ano_mes"].astype(str)
    print(mensal.head(15))
    print(f"  ... ({len(mensal)} períodos no total)")

    # 3.7 - Top 10 produtos por vendas
    print("\n[ANÁLISE] Top 10 Produtos por Vendas:")
    top10_vendas = df.groupby("product_name")["sales"].sum().sort_values(ascending=False).head(10)
    print(top10_vendas)

    # 3.8 - Top 10 produtos por lucro
    print("\n[ANÁLISE] Top 10 Produtos por Lucro:")
    top10_lucro = df.groupby("product_name")["profit"].sum().sort_values(ascending=False).head(10)
    print(top10_lucro)

    # 3.9 - Análise por Sub-Categoria
    print("\n[ANÁLISE] Análise por Sub-Categoria:")
    sub_categoria = df.groupby("sub_category").agg({
        "sales": "sum",
        "profit": "sum",
        "quantity": "sum"
    }).sort_values(by="sales", ascending=False)
    print(sub_categoria)

    # 3.10 - Correlação entre variáveis numéricas
    print("\n[ANÁLISE] Correlação entre variáveis numéricas:")
    colunas_corr = ["sales", "quantity", "discount", "profit"]
    matriz_corr = df[colunas_corr].corr()
    print(matriz_corr.round(4))

    # Retorna os dados processados para uso na etapa de visualização
    return {
        "categoria": categoria,
        "segmento": segmento,
        "regiao": regiao,
        "mensal": mensal,
        "top10_vendas": top10_vendas,
        "top10_lucro": top10_lucro,
        "sub_categoria": sub_categoria,
        "matriz_corr": matriz_corr,
    }


# =====================================================================
# ETAPA 4: VISUALIZAÇÕES GRÁFICAS
# =====================================================================
def etapa4_visualizacoes(df, resultados):
    """Gera e salva todos os gráficos da análise."""
    imprimir_separador("ETAPA 4: VISUALIZAÇÕES GRÁFICAS")

    # 4.1 - Gráfico de barras: Vendas por Categoria
    print("[GRÁFICO] Gerando: Vendas por Categoria...")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=resultados["categoria"].index,
        y="sales",
        data=resultados["categoria"],
        ax=ax,
        palette="Blues_d"
    )
    ax.set_title("Vendas por Categoria", fontsize=16, fontweight="bold")
    ax.set_xlabel("Categoria", fontsize=12)
    ax.set_ylabel("Vendas ($)", fontsize=12)
    for p in ax.patches:
        ax.annotate(f"${p.get_height():,.0f}",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="bottom", fontsize=10)
    salvar_grafico(fig, "01_vendas_por_categoria.png")

    # 4.2 - Gráfico de barras: Lucro por Categoria
    print("[GRÁFICO] Gerando: Lucro por Categoria...")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=resultados["categoria"].index,
        y="profit",
        data=resultados["categoria"],
        ax=ax,
        palette="Greens_d"
    )
    ax.set_title("Lucro por Categoria", fontsize=16, fontweight="bold")
    ax.set_xlabel("Categoria", fontsize=12)
    ax.set_ylabel("Lucro ($)", fontsize=12)
    for p in ax.patches:
        ax.annotate(f"${p.get_height():,.0f}",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="bottom", fontsize=10)
    salvar_grafico(fig, "02_lucro_por_categoria.png")

    # 4.3 - Gráfico de pizza: Vendas por Segmento
    print("[GRÁFICO] Gerando: Vendas por Segmento (Pizza)...")
    fig, ax = plt.subplots(figsize=(8, 8))
    vendas_segmento = resultados["segmento"]["sales"]
    cores = sns.color_palette("Set2", len(vendas_segmento))
    ax.pie(
        vendas_segmento.values,
        labels=vendas_segmento.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores,
        explode=[0.03] * len(vendas_segmento),
        shadow=True
    )
    ax.set_title("Distribuição de Vendas por Segmento", fontsize=16, fontweight="bold")
    salvar_grafico(fig, "03_vendas_por_segmento_pizza.png")

    # 4.4 - Gráfico de barras: Vendas por Região
    print("[GRÁFICO] Gerando: Vendas por Região...")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=resultados["regiao"].index,
        y="sales",
        data=resultados["regiao"],
        ax=ax,
        palette="Oranges_d"
    )
    ax.set_title("Vendas por Região", fontsize=16, fontweight="bold")
    ax.set_xlabel("Região", fontsize=12)
    ax.set_ylabel("Vendas ($)", fontsize=12)
    for p in ax.patches:
        ax.annotate(f"${p.get_height():,.0f}",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="bottom", fontsize=10)
    salvar_grafico(fig, "04_vendas_por_regiao.png")

    # 4.5 - Gráfico de dispersão: Desconto vs Lucro
    print("[GRÁFICO] Gerando: Dispersão Discount vs Profit...")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df,
        x="discount",
        y="profit",
        hue="category",
        palette="Set1",
        alpha=0.6,
        ax=ax
    )
    ax.axhline(y=0, color="red", linestyle="--", linewidth=1, label="Lucro Zero")
    ax.set_title("Relação entre Desconto e Lucro", fontsize=16, fontweight="bold")
    ax.set_xlabel("Desconto", fontsize=12)
    ax.set_ylabel("Lucro ($)", fontsize=12)
    ax.legend(title="Categoria")
    salvar_grafico(fig, "05_discount_vs_profit.png")

    # 4.6 - Gráfico de linha: Tendência mensal de Vendas e Lucro
    print("[GRÁFICO] Gerando: Tendência Mensal (Vendas e Lucro)...")
    mensal = resultados["mensal"]
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(mensal["ano_mes"], mensal["sales"], marker="o", label="Vendas", color="#1f77b4")
    ax.plot(mensal["ano_mes"], mensal["profit"], marker="s", label="Lucro", color="#2ca02c")
    ax.set_title("Tendência Mensal de Vendas e Lucro", fontsize=16, fontweight="bold")
    ax.set_xlabel("Ano-Mês", fontsize=12)
    ax.set_ylabel("Valor ($)", fontsize=12)
    ax.legend()
    # Rotaciona os rótulos do eixo X para melhor visualização
    plt.xticks(rotation=90, fontsize=7)
    salvar_grafico(fig, "06_tendencia_mensal.png")

    # 4.7 - Gráfico de barras horizontal: Top 10 Produtos por Vendas
    print("[GRÁFICO] Gerando: Top 10 Produtos por Vendas...")
    top10_v = resultados["top10_vendas"].sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(
        x=top10_v.values,
        y=top10_v.index,
        ax=ax,
        palette="viridis"
    )
    ax.set_title("Top 10 Produtos por Vendas", fontsize=16, fontweight="bold")
    ax.set_xlabel("Vendas ($)", fontsize=12)
    ax.set_ylabel("Produto", fontsize=12)
    for p in ax.patches:
        ax.annotate(f"${p.get_width():,.0f}",
                    (p.get_width(), p.get_y() + p.get_height() / 2.),
                    ha="left", va="center", fontsize=9, xytext=(5, 0),
                    textcoords="offset points")
    salvar_grafico(fig, "07_top10_produtos_vendas.png")

    # 4.8 - Heatmap: Matriz de Correlação
    print("[GRÁFICO] Gerando: Heatmap da Matriz de Correlação...")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        resultados["matriz_corr"],
        annot=True,
        cmap="coolwarm",
        center=0,
        fmt=".4f",
        linewidths=0.5,
        ax=ax,
        square=True
    )
    ax.set_title("Matriz de Correlação - Variáveis Numéricas", fontsize=14, fontweight="bold")
    salvar_grafico(fig, "08_heatmap_correlacao.png")

    # 4.9 - Gráfico de barras: Lucro por Sub-Categoria (colorido por positivo/negativo)
    print("[GRÁFICO] Gerando: Lucro por Sub-Categoria (positivo/negativo)...")
    sub_cat_profit = resultados["sub_categoria"]["profit"].sort_values(ascending=True)
    # Define cores: verde para lucro positivo, vermelho para negativo
    cores_sub = ["#d62728" if v < 0 else "#2ca02c" for v in sub_cat_profit.values]
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(
        x=sub_cat_profit.values,
        y=sub_cat_profit.index,
        ax=ax,
        palette=cores_sub
    )
    ax.axvline(x=0, color="black", linestyle="-", linewidth=0.8)
    ax.set_title("Lucro por Sub-Categoria (Verde = Positivo | Vermelho = Negativo)",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Lucro ($)", fontsize=12)
    ax.set_ylabel("Sub-Categoria", fontsize=12)
    salvar_grafico(fig, "09_lucro_por_subcategoria.png")


# =====================================================================
# ETAPA 5: ANÁLISE LOGÍSTICA (Perspectiva de Otimização)
# Autor: Filippe Borba - Logistics Transformation Engineer
# =====================================================================
def etapa5_analise_logistica(df):
    """
    Análise sob a perspectiva de Otimização Logística.
    Avalia lead time de entrega, eficiência dos modos de envio,
    consolidação de pedidos, giro de estoque e eficiência por região.
    """
    imprimir_separador("ETAPA 5: ANÁLISE LOGÍSTICA (OTIMIZAÇÃO DE ENTREGAS)")

    # -----------------------------------------------------------------
    # 5.1 - ANÁLISE DE LEAD TIME DE ENTREGA (Tempo de Entrega)
    # -----------------------------------------------------------------
    print("[ANÁLISE] 5.1 - Lead Time de Entrega (Tempo entre Pedido e Envio)")

    # Calcula o lead time em dias (diferença entre envio e pedido)
    df["delivery_lead_time"] = (df["ship_date"] - df["order_date"]).dt.days

    # Estatísticas gerais do lead time
    print("\n  Estatísticas do Lead Time de Entrega (dias):")
    print(f"    Média:   {df['delivery_lead_time'].mean():.2f} dias")
    print(f"    Mediana: {df['delivery_lead_time'].median():.2f} dias")
    print(f"    Mínimo:  {df['delivery_lead_time'].min()} dias")
    print(f"    Máximo:  {df['delivery_lead_time'].max()} dias")
    print(f"    Desvio Padrão: {df['delivery_lead_time'].std():.2f} dias")

    # Lead time médio por modo de envio
    print("\n  Lead Time médio por Modo de Envio (Ship Mode):")
    lead_time_ship_mode = df.groupby("ship_mode")["delivery_lead_time"].agg(
        ["mean", "median", "min", "max", "count"]
    ).round(2)
    lead_time_ship_mode.columns = ["Média (dias)", "Mediana (dias)", "Mínimo", "Máximo", "Qtd. Pedidos"]
    print(lead_time_ship_mode)

    # -----------------------------------------------------------------
    # 5.2 - EFICIÊNCIA POR MODO DE ENVIO (Ship Mode)
    # -----------------------------------------------------------------
    print("\n[ANÁLISE] 5.2 - Eficiência por Modo de Envio (Ship Mode)")

    # Agrupamento por modo de envio com métricas financeiras e operacionais
    eficiencia_ship_mode = df.groupby("ship_mode").agg(
        vendas_totais=("sales", "sum"),
        lucro_total=("profit", "sum"),
        quantidade_total=("quantity", "sum"),
        qtd_pedidos=("order_id", "count"),
    ).round(2)

    # Cálculo da margem de lucro (%) por modo de envio
    eficiencia_ship_mode["margem_lucro_%"] = (
        (eficiencia_ship_mode["lucro_total"] / eficiencia_ship_mode["vendas_totais"]) * 100
    ).round(2)

    # Margem de lucro média por pedido
    eficiencia_ship_mode["margem_media_por_pedido"] = (
        eficiencia_ship_mode["lucro_total"] / eficiencia_ship_mode["qtd_pedidos"]
    ).round(2)

    print("\n  Eficiência por Modo de Envio:")
    print(eficiencia_ship_mode)

    # Identifica o modo de envio mais lucrativo por pedido
    melhor_margem_pedido = eficiencia_ship_mode["margem_media_por_pedido"].idxmax()
    melhor_margem_pct = eficiencia_ship_mode["margem_lucro_%"].idxmax()
    print(f"\n  -> Modo de envio com maior margem média por pedido: '{melhor_margem_pedido}' "
          f"(${eficiencia_ship_mode.loc[melhor_margem_pedido, 'margem_media_por_pedido']:.2f}/pedido)")
    print(f"  -> Modo de envio com maior margem de lucro (%): '{melhor_margem_pct}' "
          f"({eficiencia_ship_mode.loc[melhor_margem_pct, 'margem_lucro_%']:.2f}%)")

    # -----------------------------------------------------------------
    # 5.3 - LEAD TIME POR REGIÃO
    # -----------------------------------------------------------------
    print("\n[ANÁLISE] 5.3 - Lead Time por Região (Identificação de Gargalos Logísticos)")

    lead_time_regiao = df.groupby("region").agg(
        lead_time_medio=("delivery_lead_time", "mean"),
        lead_time_mediano=("delivery_lead_time", "median"),
        vendas_totais=("sales", "sum"),
        lucro_total=("profit", "sum"),
        qtd_pedidos=("order_id", "count"),
    ).round(2)

    print("\n  Lead Time e Desempenho por Região:")
    print(lead_time_regiao)

    # Identifica a região com maior lead time médio (potencial gargalo logístico)
    regiao_maior_lead = lead_time_regiao["lead_time_medio"].idxmax()
    regiao_menor_lead = lead_time_regiao["lead_time_medio"].idxmin()
    print(f"\n  -> Região com MAIOR lead time médio: '{regiao_maior_lead}' "
          f"({lead_time_regiao.loc[regiao_maior_lead, 'lead_time_medio']:.2f} dias) - POTENCIAL GARGALO")
    print(f"  -> Região com MENOR lead time médio: '{regiao_menor_lead}' "
          f"({lead_time_regiao.loc[regiao_menor_lead, 'lead_time_medio']:.2f} dias) - MAIS EFICIENTE")

    # -----------------------------------------------------------------
    # 5.4 - ANÁLISE DE CONSOLIDAÇÃO DE PEDIDOS
    # -----------------------------------------------------------------
    print("\n[ANÁLISE] 5.4 - Consolidação de Pedidos (Itens por Pedido)")

    # Conta quantos itens (linhas) existem por order_id
    itens_por_pedido = df.groupby("order_id").size()

    # Estatísticas de consolidação de pedidos
    print("\n  Estatísticas de Itens por Pedido:")
    print(f"    Média de itens por pedido: {itens_por_pedido.mean():.2f}")
    print(f"    Mediana de itens por pedido: {itens_por_pedido.median():.2f}")
    print(f"    Máximo de itens em um pedido: {itens_por_pedido.max()}")
    print(f"    Mínimo de itens em um pedido: {itens_por_pedido.min()}")
    print(f"    Total de pedidos únicos: {len(itens_por_pedido)}")

    # Top 10 pedidos com mais itens (maior consolidação)
    print("\n  Top 10 Pedidos com Mais Itens (Maior Consolidação):")
    top10_pedidos = itens_por_pedido.sort_values(ascending=False).head(10)
    top10_pedidos_df = top10_pedidos.to_frame(name="qtd_itens")
    top10_pedidos_df["qtd_itens"] = top10_pedidos_df["qtd_itens"].astype(int)
    print(top10_pedidos_df)

    # -----------------------------------------------------------------
    # 5.5 - GIRO DE ESTOQUE POR SUB-CATEGORIA
    # -----------------------------------------------------------------
    print("\n[ANÁLISE] 5.5 - Giro de Estoque por Sub-Categoria (Fast-moving vs Slow-moving)")

    giro_estoque = df.groupby("sub_category").agg(
        quantidade_total=("quantity", "sum"),
        produtos_unicos=("product_name", "nunique"),
        vendas_totais=("sales", "sum"),
    ).round(2)

    # Quantidade média vendida por produto (indicador de giro de estoque)
    giro_estoque["qtd_media_por_produto"] = (
        giro_estoque["quantidade_total"] / giro_estoque["produtos_unicos"]
    ).round(2)

    # Ordena pelo giro de estoque (quantidade média por produto)
    giro_estoque = giro_estoque.sort_values(by="qtd_media_por_produto", ascending=False)

    print("\n  Giro de Estoque por Sub-Categoria:")
    print(giro_estoque)

    # Identifica sub-categorias fast-moving e slow-moving
    sub_fast = giro_estoque["qtd_media_por_produto"].idxmax()
    sub_slow = giro_estoque["qtd_media_por_produto"].idxmin()
    print(f"\n  -> Sub-categoria FAST-MOVING (maior giro): '{sub_fast}' "
          f"({giro_estoque.loc[sub_fast, 'qtd_media_por_produto']:.2f} un/produto)")
    print(f"  -> Sub-categoria SLOW-MOVING (menor giro): '{sub_slow}' "
          f"({giro_estoque.loc[sub_slow, 'qtd_media_por_produto']:.2f} un/produto)")

    # -----------------------------------------------------------------
    # 5.6 - MARGEM DE LUCRO POR MODO DE ENVIO VS REGIÃO (Cross-Analysis)
    # -----------------------------------------------------------------
    print("\n[ANÁLISE] 5.6 - Margem de Lucro por Modo de Envio vs Região (Cross-Analysis)")

    # Calcula a margem de lucro por linha antes de agregar
    df["profit_margin"] = (df["profit"] / df["sales"]) * 100

    # Tabela pivot: modos de envio (linhas) vs regiões (colunas), valores = margem de lucro média
    pivot_margem = df.pivot_table(
        index="ship_mode",
        columns="region",
        values="profit_margin",
        aggfunc="mean"
    ).round(2)

    print("\n  Margem de Lucro Média (%) por Ship Mode vs Região:")
    print(pivot_margem)

    # -----------------------------------------------------------------
    # 5.7 - VISUALIZAÇÕES LOGÍSTICAS
    # -----------------------------------------------------------------
    print("\n[GRÁFICOS] Gerando visualizações logísticas...")

    # Gráfico 10 - Lead Time médio por Ship Mode
    print("[GRÁFICO] Gerando: Lead Time médio por Ship Mode...")
    lead_sm = df.groupby("ship_mode")["delivery_lead_time"].mean().sort_values().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=lead_sm,
        x="ship_mode",
        y="delivery_lead_time",
        hue="ship_mode",
        palette="Blues_d",
        ax=ax
    )
    ax.set_title("Lead Time Médio de Entrega por Modo de Envio", fontsize=16, fontweight="bold")
    ax.set_xlabel("Modo de Envio (Ship Mode)", fontsize=12)
    ax.set_ylabel("Lead Time Médio (dias)", fontsize=12)
    ax.legend(title="Modo de Envio", loc="upper left")
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="bottom", fontsize=10)
    salvar_grafico(fig, "10_lead_time_por_ship_mode.png")

    # Gráfico 11 - Lead Time médio por Região
    print("[GRÁFICO] Gerando: Lead Time médio por Região...")
    lead_reg = df.groupby("region")["delivery_lead_time"].mean().sort_values().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=lead_reg,
        x="region",
        y="delivery_lead_time",
        hue="region",
        palette="Oranges_d",
        ax=ax
    )
    ax.set_title("Lead Time Médio de Entrega por Região", fontsize=16, fontweight="bold")
    ax.set_xlabel("Região", fontsize=12)
    ax.set_ylabel("Lead Time Médio (dias)", fontsize=12)
    ax.legend(title="Região", loc="upper left")
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="bottom", fontsize=10)
    salvar_grafico(fig, "11_lead_time_por_regiao.png")

    # Gráfico 12 - Margem de Lucro por Ship Mode
    print("[GRÁFICO] Gerando: Margem de Lucro por Ship Mode...")
    margem_sm = eficiencia_ship_mode["margem_lucro_%"].sort_values().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=margem_sm,
        x="ship_mode",
        y="margem_lucro_%",
        hue="ship_mode",
        palette="Greens_d",
        ax=ax
    )
    ax.set_title("Margem de Lucro (%) por Modo de Envio", fontsize=16, fontweight="bold")
    ax.set_xlabel("Modo de Envio (Ship Mode)", fontsize=12)
    ax.set_ylabel("Margem de Lucro (%)", fontsize=12)
    ax.legend(title="Modo de Envio", loc="upper left")
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}%",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="bottom", fontsize=10)
    salvar_grafico(fig, "12_margem_lucro_por_ship_mode.png")

    # Gráfico 13 - Heatmap: Margem de Lucro por Ship Mode vs Região
    print("[GRÁFICO] Gerando: Heatmap Margem de Lucro por Ship Mode vs Região...")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        pivot_margem,
        annot=True,
        cmap="RdYlGn",
        center=0,
        fmt=".2f",
        linewidths=0.5,
        ax=ax,
        cbar_kws={"label": "Margem de Lucro (%)"}
    )
    ax.set_title("Margem de Lucro (%) por Modo de Envio vs Região",
                 fontsize=14, fontweight="bold")
    ax.set_xlabel("Região", fontsize=12)
    ax.set_ylabel("Modo de Envio (Ship Mode)", fontsize=12)
    salvar_grafico(fig, "13_heatmap_margem_ship_mode_vs_regiao.png")

    # -----------------------------------------------------------------
    # 5.8 - INSIGHTS LOGÍSTICOS (Resumo para Console)
    # -----------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  INSIGHTS LOGÍSTICOS - RESUMO EXECUTIVO")
    print("-" * 70)

    # Insight 1: Modo de envio com melhor margem
    print(f"\n  1. MODO DE ENVIO MAIS LUCRATIVO:")
    print(f"     -> '{melhor_margem_pct}' apresenta a maior margem de lucro "
          f"({eficiencia_ship_mode.loc[melhor_margem_pct, 'margem_lucro_%']:.2f}%).")
    print(f"     -> '{melhor_margem_pedido}' tem a maior margem média por pedido "
          f"(${eficiencia_ship_mode.loc[melhor_margem_pedido, 'margem_media_por_pedido']:.2f}/pedido).")

    # Insight 2: Região com maior lead time (gargalo)
    print(f"\n  2. GARGALO LOGÍSTICO POR REGIÃO:")
    print(f"     -> '{regiao_maior_lead}' tem o maior lead time médio "
          f"({lead_time_regiao.loc[regiao_maior_lead, 'lead_time_medio']:.2f} dias).")
    print(f"     -> '{regiao_menor_lead}' é a mais eficiente "
          f"({lead_time_regiao.loc[regiao_menor_lead, 'lead_time_medio']:.2f} dias).")
    print(f"     -> Diferença de lead time entre regiões: "
          f"{lead_time_regiao['lead_time_medio'].max() - lead_time_regiao['lead_time_medio'].min():.2f} dias.")

    # Insight 3: Consolidação de pedidos
    print(f"\n  3. CONSOLIDAÇÃO DE PEDIDOS:")
    print(f"     -> Média de {itens_por_pedido.mean():.2f} itens por pedido.")
    print(f"     -> Pedido com maior consolidação: {itens_por_pedido.max()} itens.")
    print(f"     -> Oportunidade: pedidos com múltiplos itens podem otimizar custos de frete.")

    # Insight 4: Giro de estoque
    print(f"\n  4. GIRO DE ESTOQUE POR SUB-CATEGORIA:")
    print(f"     -> Fast-moving: '{sub_fast}' "
          f"({giro_estoque.loc[sub_fast, 'qtd_media_por_produto']:.2f} un/produto).")
    print(f"     -> Slow-moving: '{sub_slow}' "
          f"({giro_estoque.loc[sub_slow, 'qtd_media_por_produto']:.2f} un/produto).")
    print(f"     -> Recomendação: manter maior estoque de segurança para '{sub_fast}'.")

    # Insight 5: Cross-analysis margem por região e modo de envio
    melhor_combinacao = pivot_margem.stack().idxmax()
    pior_combinacao = pivot_margem.stack().idxmin()
    print(f"\n  5. EFICIÊNCIA LOGÍSTICA (SHIP MODE x REGIÃO):")
    print(f"     -> Melhor combinação: '{melhor_combinacao[0]}' na região '{melhor_combinacao[1]}' "
          f"({pivot_margem.loc[melhor_combinacao]:.2f}%).")
    print(f"     -> Pior combinação: '{pior_combinacao[0]}' na região '{pior_combinacao[1]}' "
          f"({pivot_margem.loc[pior_combinacao]:.2f}%).")

    print("\n" + "-" * 70)
    print("  [CONCLUÍDO] Análise Logística finalizada.")
    print("-" * 70)

    # Retorna o DataFrame com a nova coluna delivery_lead_time adicionada
    return df


# =====================================================================
# FUNÇÃO PRINCIPAL
# =====================================================================
def main():
    """Função principal que orquestra todas as etapas da análise."""
    print("#" * 70)
    print("#  ANÁLISE EXPLORATÓRIA DE DADOS - SAMPLE SUPERSTORE")
    print("#  Desafio de Data Science")
    print("#" * 70)

    # Cria a pasta de gráficos
    criar_pasta_graficos()

    try:
        # ETAPA 1: Importação e compreensão dos dados
        df = etapa1_importacao_compreensao()

        # ETAPA 2: Tratamento e preparação dos dados
        df = etapa2_tratamento_preparacao(df)

        # ETAPA 3: Análise exploratória
        resultados = etapa3_analise_exploratoria(df)

        # ETAPA 4: Visualizações gráficas
        etapa4_visualizacoes(df, resultados)

        # ETAPA 5: Análise Logística (Perspectiva de Otimização - Filippe Borba)
        df = etapa5_analise_logistica(df)

        # -----------------------------------------------------------------
        # RESUMO FINAL DOS ARQUIVOS GERADOS
        # -----------------------------------------------------------------
        imprimir_separador("RESUMO FINAL - ARQUIVOS GERADOS")
        print(f"Total de gráficos gerados: {len(arquivos_gerados)}")
        print(f"Pasta de destino: {GRAFICOS_DIR}\n")
        for i, arquivo in enumerate(arquivos_gerados, 1):
            caminho = os.path.join(GRAFICOS_DIR, arquivo)
            tamanho = os.path.getsize(caminho) / 1024  # em KB
            print(f"  {i:02d}. {arquivo} ({tamanho:.1f} KB)")

        print("\n[CONCLUÍDO] Análise Exploratória finalizada com sucesso!")
        print("#" * 70)

    except FileNotFoundError as e:
        print("\n[ERRO] Arquivo não encontrado!")
        print(f"{e}")
        print("\nSolução: Coloque o arquivo 'Sample - Superstore.csv' na mesma pasta do script.")
    except Exception as e:
        print(f"\n[ERRO] Ocorreu um erro durante a execução: {e}")
        raise


# ---------------------------------------------------------------------
# PONTO DE ENTRADA DO SCRIPT
# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()