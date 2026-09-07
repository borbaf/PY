from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import os
import kagglehub
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import numpy as np

from kagglehub import KaggleDatasetAdapter

import warnings
warnings.filterwarnings('ignore')


df = kagglehub.dataset_load(
    KaggleDatasetAdapter.PANDAS,
    "mohammadtalib786/retail-sales-dataset",
    "retail_sales_dataset.csv",
    pandas_kwargs={
        "encoding": "latin-1",
        "engine": "python",
        "on_bad_lines": "skip",
    },
)

# Criar banco em memória
conn = sqlite3.connect(":memory:")

df.to_sql("vendas", conn)

# df.info()
# print("Shape:", df.shape)
# print(df.head())

CSC = """

SELECT Age, 
       SUM("Total Amount") AS Total_Compras 
       FROM vendas  
       GROUP BY Age 
       ORDER BY Total_Compras DESC
"""



print("\nTotal de compras por idade:\n")
print(pd.read_sql(CSC, conn))
conn.close()