# ============================================================================
# Arquivo: db_connection.py
# ============================================================================
#"""Módulo responsável pela conexão com o banco de dados PostgreSQL."""

import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Cria e retorna uma conexão com o banco de dados PostgreSQL.

    Args:
        db_name (str): Nome do banco de dados.
        db_user (str): Usuário do banco de dados.
        db_password (str): Senha do banco de dados.
        db_host (str): Host do banco de dados.
        db_port (str): Porta do banco de dados.

    Returns:
        connection: Objeto de conexão ou None em caso de erro.
    """
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Conexão com o PostgreSQL bem-sucedida.")
    except OperationalError as erro:
        print(f"Erro ao conectar ao PostgreSQL: {erro}")
    return connection


def close_connection(connection):
    """Fecha a conexão com o banco de dados.

    Args:
        connection: Objeto de conexão a ser fechado.
    """
    if connection is not None:
        connection.close()
        print("Conexão fechada.")


# ============================================================================
# Fim do arquivo: db_connection.py
# ============================================================================


# ============================================================================
# Arquivo: db_create_table.py
# ============================================================================
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


# ============================================================================
# Fim do arquivo: db_create_table.py
# ============================================================================


# ============================================================================
# Arquivo: db_insert.py
# ============================================================================
#"""Módulo responsável por operações de inserção no banco de dados."""


def insert_usuario(connection, nome, email, idade):
    """Insere um novo usuário na tabela 'usuarios'.

    Args:
        connection: Objeto de conexão com o banco.
        nome (str): Nome do usuário.
        email (str): E-mail do usuário.
        idade (int): Idade do usuário.

    Returns:
        int or None: ID do registro inserido ou None em caso de erro.
    """
    insert_query = """
    INSERT INTO usuarios (nome, email, idade)
    VALUES (%s, %s, %s)
    RETURNING id;
    """

    try:
        cursor = connection.cursor()
        cursor.execute(insert_query, (nome, email, idade))
        usuario_id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        print(f"Usuário '{nome}' inserido com sucesso. ID: {usuario_id}")
        return usuario_id
    except Exception as erro:
        print(f"Erro ao inserir usuário '{nome}': {erro}")
        connection.rollback()
        return None


# ============================================================================
# Fim do arquivo: db_insert.py
# ============================================================================


# ============================================================================
# Arquivo: db_select.py
# ============================================================================
#"""Módulo responsável por operações de seleção no banco de dados."""


def select_usuarios(connection):
    """Seleciona e retorna todos os usuários cadastrados.

    Args:
        connection: Objeto de conexão com o banco.

    Returns:
        list: Lista de tuplas contendo os registros dos usuários.
    """
    select_query = "SELECT id, nome, email, idade, criado_em FROM usuarios ORDER BY id;"

    try:
        cursor = connection.cursor()
        cursor.execute(select_query)
        registros = cursor.fetchall()
        cursor.close()

        print("Usuários cadastrados:")
        print("-" * 60)
        for registro in registros:
            print(f"ID: {registro[0]} | Nome: {registro[1]} | "
                  f"E-mail: {registro[2]} | Idade: {registro[3]} | "
                  f"Criado em: {registro[4]}")
        print("-" * 60)
        return registros
    except Exception as erro:
        print(f"Erro ao selecionar usuários: {erro}")
        return []


def select_usuario_por_id(connection, usuario_id):
    """Seleciona um usuário específico pelo ID.

    Args:
        connection: Objeto de conexão com o banco.
        usuario_id (int): ID do usuário a ser buscado.

    Returns:
        tuple or None: Registro do usuário ou None se não encontrado.
    """
    select_query = "SELECT id, nome, email, idade, criado_em FROM usuarios WHERE id = %s;"

    try:
        cursor = connection.cursor()
        cursor.execute(select_query, (usuario_id,))
        registro = cursor.fetchone()
        cursor.close()

        if registro:
            print(f"Usuário encontrado: ID: {registro[0]} | "
                  f"Nome: {registro[1]} | E-mail: {registro[2]} | "
                  f"Idade: {registro[3]} | Criado em: {registro[4]}")
        else:
            print(f"Nenhum usuário encontrado com ID {usuario_id}.")
        return registro
    except Exception as erro:
        print(f"Erro ao selecionar usuário com ID {usuario_id}: {erro}")
        return None


# ============================================================================
# Fim do arquivo: db_select.py
# ============================================================================


# ============================================================================
# Arquivo: db_update.py
# ============================================================================
#"""Módulo responsável por operações de atualização no banco de dados."""


def update_usuario(connection, usuario_id, nome=None, email=None, idade=None):
    """Atualiza os dados de um usuário existente.

    Apenas os campos fornecidos (diferentes de None) serão atualizados.

    Args:
        connection: Objeto de conexão com o banco.
        usuario_id (int): ID do usuário a ser atualizado.
        nome (str, optional): Novo nome do usuário.
        email (str, optional): Novo e-mail do usuário.
        idade (int, optional): Nova idade do usuário.

    Returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário.
    """
    campos = []
    valores = []

    if nome is not None:
        campos.append("nome = %s")
        valores.append(nome)
    if email is not None:
        campos.append("email = %s")
        valores.append(email)
    if idade is not None:
        campos.append("idade = %s")
        valores.append(idade)

    if not campos:
        print("Nenhum campo fornecido para atualização.")
        return False

    valores.append(usuario_id)
    update_query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = %s;"

    try:
        cursor = connection.cursor()
        cursor.execute(update_query, tuple(valores))
        linhas_afetadas = cursor.rowcount
        connection.commit()
        cursor.close()

        if linhas_afetadas > 0:
            print(f"Usuário ID {usuario_id} atualizado com sucesso. "
                  f"Linhas afetadas: {linhas_afetadas}")
            return True
        else:
            print(f"Nenhum usuário encontrado com ID {usuario_id} para atualização.")
            return False
    except Exception as erro:
        print(f"Erro ao atualizar usuário ID {usuario_id}: {erro}")
        connection.rollback()
        return False


# ============================================================================
# Fim do arquivo: db_update.py
# ============================================================================


# ============================================================================
# Arquivo: main.py
# ============================================================================
#"""Arquivo principal que integra todas as operações de banco de dados.

Este script demonstra o uso dos módulos de conexão, criação de tabela,
inserção, seleção e atualização no PostgreSQL.
"""

# Importações dos módulos criados
# from db_connection import create_connection, close_connection
# from db_create_table import create_table
# from db_insert import insert_usuario
# from db_select import select_usuarios, select_usuario_por_id
# from db_update import update_usuario


def main():
    """Função principal que executa o fluxo completo de operações."""
    # Configurações do banco de dados
    DB_NAME = "meu_banco"
    DB_USER = "postgres"
    DB_PASSWORD = "senha123"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    # 1. Criar conexão
    connection = create_connection(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    if connection is None:
        print("Não foi possível estabelecer conexão. Encerrando.")
        return

    try:
        # 2. Criar tabela
        create_table(connection, table_name="usuarios")

        # 3. Inserir usuários
        insert_usuario(connection, nome="Alice Souza", email="alice@example.com", idade=28)
        insert_usuario(connection, nome="Bruno Lima", email="bruno@example.com", idade=34)
        insert_usuario(connection, nome="Carla Dias", email="carla@example.com", idade=22)

        # 4. Selecionar todos os usuários
        print("\n--- Listando todos os usuários ---")
        select_usuarios(connection)

        # 5. Selecionar usuário por ID
        print("\n--- Buscando usuário por ID ---")
        select_usuario_por_id(connection, usuario_id=1)

        # 6. Atualizar usuário
        print("\n--- Atualizando usuário ---")
        update_usuario(connection, usuario_id=1, nome="Alice Souza Lima", idade=29)

        # 7. Selecionar novamente para confirmar atualização
        print("\n--- Listando usuários após atualização ---")
        select_usuarios(connection)

    finally:
        # 8. Fechar conexão
        close_connection(connection)


if __name__ == "__main__":
    main()


# ============================================================================
# Fim do arquivo: main.py
# ============================================================================