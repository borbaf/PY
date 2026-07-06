#"""Módulo responsável pela criação de tabelas no banco de dados."""


def create_table(connection, table_name="usuarios"):
    """Cria uma tabela no banco de dados.

    Args:
        connection: Objeto de conexão com o banco.
        table_name (str): Nome da tabela a ser criada.

    Returns:
        bool: True se a tabela foi criada com sucesso, False caso contrário.
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        idade INTEGER,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print(f"Tabela '{table_name}' criada com sucesso.")
        return True
    except Exception as erro:
        print(f"Erro ao criar a tabela '{table_name}': {erro}")
        connection.rollback()
        return False
