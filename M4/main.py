import psycopg2
from psycopg2 import sql


conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="P$inUca01"
)

conn.autocommit = True

#definir novo Banco de Dados
db_name = "db_borbaf"

#Criar uma sting SQL para ser executada
create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))

#Construindo um cursor para executar a query
cursor = conn.cursor()
cursor.execute(create_db_query)

#fechar o cursor e a conexão
cursor.close()
conn.close()

print(f"Banco de dados '{db_name}' criado com sucesso!")