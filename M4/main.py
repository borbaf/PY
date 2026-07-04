import psycopg2
from psycopg2 import sql


conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="db_borbaf",
    user="postgres",
    password="P$inUca01"
)

conn.autocommit = True

#definir novo Banco de Dados
#db_name = "postgres"

#Criar uma sting SQL para ser executada
#create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))

#Construindo um cursor para executar a query
#cursor = conn.cursor()
#cursor.execute(create_db_query)

#fechar o cursor e a conexão
#cursor.close()
#conn.close()

#print(f"Banco de dados '{db_name}' criado com sucesso!")


# create_table_query = '''
#     CREATE TABLE nome_tabela (
#     coluna1 VARCHAR(255),
#     coluna2 VARCHAR(255)
#     )
# '''
# cursor = conn.cursor()
# cursor.execute(create_table_query)
# conn.commit()

# cursor.close()
# conn.close()

# print("Tabela criada com sucesso!")


def create_table(connection):
    """Executa o CREATE TABLE corrigido no banco de dados."""
    cursor = connection.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    connection.commit()
    cursor.close()



#INSERT

insert_query = '''
    INSERT INTO nome_tabela (coluna1, coluna2) VALUES (%s, %s)
'''
cursor = conn.cursor()
cursor.execute(insert_query, ("valor1", "valor2"))
conn.commit()

cursor.close()
conn.close()

print("Dados inseridos com sucesso!")


#SELECT

cur.execute("SELECT * FROM nome_tabela")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()