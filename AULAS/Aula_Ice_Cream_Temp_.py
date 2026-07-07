import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Caminho local genérico para o arquivo CSV
csv_path = 'Ice Cream Sales - temperatures.csv'

# Carregar o dataset
try:
    df = pd.read_csv(csv_path)
    print("Dataset carregado com sucesso!")
    print(f"Formato: {df.shape}")
    print(df.head())
except FileNotFoundError:
    raise FileNotFoundError(
        f"Arquivo '{csv_path}' não encontrado. "
        "Certifique-se de que o arquivo CSV está na mesma pasta do script."
        )


# Ordena do mais frio para o mais quente (Crescente)
df_ordenado = df.sort_values(by="Temperature", ascending=True)

print(df_ordenado.head())
