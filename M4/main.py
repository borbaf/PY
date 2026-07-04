import psycopg2
from psycopg2 import sql


conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="db_borbaf",
    user="postgres",
    password="P$inUca01" #Senha Padrão para uso do PostgreSQL 15.3
)

conn.autocommit = True

#definir novo Banco de Dados
#db_name = "postgres"

#Criar uma sting SQL para ser executada
#create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))

#Construindo um cursor para executar a query
#cur = conn.cursor()

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
    cur = connection.cursor()
    cur.execute(CREATE_TABLE_SQL)
    connection.commit()
    cur.close()



#INSERT

insert_query = '''
    INSERT INTO nome_tabela (coluna1, coluna2) VALUES (%s, %s)
'''
cur = conn.cursor()
cur.execute(insert_query, ("Texto1", "Texto2"))
conn.commit()

# cursor.close()
# conn.close()

print("Dados inseridos com sucesso!")


#SELECT

cur.execute("SELECT * FROM nome_tabela")
rows = cur.fetchall()

for row in rows:
    print(row)

# cur.close()
# conn.close()


#UPDATE

novo_valor = "NovoTexto"
valor_criterio = "Texto2"

cur.execute("UPDATE nome_tabela SET coluna1 = %s WHERE coluna2 = %s", (novo_valor, valor_criterio))
conn.commit()
cur.execute("SELECT * FROM nome_tabela")
rows = cur.fetchall()

#for row in rows:
print(row)








cur.close()
conn.close()

