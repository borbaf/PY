import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
    

# Obtém o caminho absoluto do diretório onde este script está localizado.
# __file__ é o caminho do próprio arquivo .py, os.path.abspath garante o caminho
# completo e os.path.dirname extrai apenas a pasta (sem o nome do arquivo).

diretorio_script = os.path.dirname(os.path.abspath(__file__)) 


# Junta o diretório do script com o nome do arquivo CSV, criando um caminho
# completo e independente de onde o terminal esteja executando o comando.

csv_path = os.path.join(diretorio_script, "Sample - Superstore.csv") # explicita o caminho do arquivo csv


# Carregar o dataset
try:
    df = pd.read_csv(csv_path,encoding='cp1252')
    print("Dataset carregado com sucesso!")
    print(f"Formato: {df.shape}")
    print(df.head())
except FileNotFoundError:
    raise FileNotFoundError(
        f"Arquivo '{csv_path}' não encontrado. "
        "Certifique-se de que o arquivo CSV está na mesma pasta do script."
        )


print(df.head())