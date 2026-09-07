from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd




# # String de conexao dentro de aspas duplas no Python
# client = MongoClient("mongodb+srv://borbaf_db_user:borbaF123@clusterfb.xwsr3hd.mongodb.net/")

# uri = "mongodb+srv://borbaf_db_user:borbaF123@clusterfb.xwsr3hd.mongodb.net/"
# db = client["teste_fb"]





url = "https://www.python.org/"
html = urlopen(url)


bs = BeautifulSoup(html.read(), "html.parser")

linhas = bs.find_all('tr',{"class": "medium-widget blog-widget"})

print(linhas)





# collection = db["aula"]
# data = list(collection.find())



# #Criar um DataFrame a partir dos dados obtidos do MongoDB

# df = pd.DataFrame(documentos) 
# print(f'colunas disponiveis: {df.columns.tolist()}')


# #Gerar um gráfico de linha para visualizar a relação entre peso e status dos produtos
# plt.figure(figsize=(10, 6))
# sns.countplot(x='status', data=df)
# plt.title('Distribuição de Status dos Produtos')

# plot_data = pd.DataFrame(data)
# plt.show()