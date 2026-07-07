import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


diretorio_script = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(diretorio_script, "Sample - Superstore.csv")

df = pd.read_csv(csv_path)


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


print(df.head())