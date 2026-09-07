from pymongo import MongoClient

# String de conexao dentro de aspas duplas no Python
client = MongoClient("mongodb+srv://borbaf_db_user:SENHA_REAL@clusterfb.xwsr3hd.mongodb.net/")

uri = "mongodb+srv://borbaf_db_user:SENHA_REAL@clusterfb.xwsr3hd.mongodb.net/"
db = client["teste_fb"]
print("Conectado ao MongoDB Atlas com sucesso!")


