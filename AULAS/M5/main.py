from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# String de conexao dentro de aspas duplas no Python
client = MongoClient("mongodb+srv://borbaf_db_user:borbaF123@clusterfb.xwsr3hd.mongodb.net/")

uri = "mongodb+srv://borbaf_db_user:borbaF123@clusterfb.xwsr3hd.mongodb.net/"
db = client["teste_fb"]


documentos = [
        {
            "origem": "São Paulo - SP",
            "destino": "Rio de Janeiro - RJ",
            "produto": "Eletrônicos",
            "peso": 12.5,
            "status": "em trânsito",
        },
        {
            "origem": "Belo Horizonte - MG",
            "destino": "Curitiba - PR",
            "produto": "Móveis",
            "peso": 45.0,
            "status": "entregue",
        },
        {
            "origem": "Porto Alegre - RS",
            "destino": "Florianópolis - SC",
            "produto": "Alimentos perecíveis",
            "peso": 8.3,
            "status": "aguardando coleta",
        },
        {
            "origem": "Salvador - BA",
            "destino": "Recife - PE",
            "produto": "Material de construção",
            "peso": 120.0,
            "status": "em trânsito",
        },
        {
            "origem": "Fortaleza - CE",
            "destino": "Manaus - AM",
            "produto": "Eletrodomésticos",
            "peso": 33.7,
            "status": "entregue",
        }]


collection = db["aula"]
data = list(collection.find())



#Criar um DataFrame a partir dos dados obtidos do MongoDB

df = pd.DataFrame(documentos) 
print(f'colunas disponiveis: {df.columns.tolist()}')


#Gerar um gráfico de linha para visualizar a relação entre peso e status dos produtos
plt.figure(figsize=(10, 6))
sns.countplot(x='status', data=df)
plt.title('Distribuição de Status dos Produtos')

plot_data = pd.DataFrame(data)
plt.show()