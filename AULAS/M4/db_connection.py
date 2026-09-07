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
