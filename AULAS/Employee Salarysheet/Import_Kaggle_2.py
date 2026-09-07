import os
import kagglehub
import kaggle
import sqlite3
import pandas as pd
import sqlite3
from kagglehub import KaggleDatasetAdapter
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import warnings

warnings.filterwarnings('ignore')


kaggle.api.dataset_download_files(
    "ahmdayman/retail-sales-dataset",
    path=".",
    unzip=True
)

df = pd.read_csv('retail_sales_dataset.csv')



# Criar banco em memória
conn = sqlite3.connect(":memory:")

df.info()
print("Shape:", df.shape)
print(df.head())
