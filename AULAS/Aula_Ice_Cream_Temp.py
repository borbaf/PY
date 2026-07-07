import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

# Load dataset

#df = pd.read_csv("/kaggle/input/temperature-and-ice-cream-sales/Ice Cream Sales - temperatures.csv")
#Buscar online

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


print(df.head())
