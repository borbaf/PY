# main.py
# Aplicacao principal para conexao e operacoes com o banco de dados
#
# Correcoes aplicadas:
# - Removidas todas as docstrings com aspas triplas para evitar o erro
#   'unterminated triple-quoted string literal' durante copia/colagem.
# - Utilizados apenas comentarios simples com hashtag (#).
# - Inseridas as credenciais corretas do usuario (db_borbaf, P$inUca01).

import os
import sys
import logging

try:
    import psycopg2
    from psycopg2 import OperationalError
except ImportError:
    psycopg2 = None
    OperationalError = Exception

# Configuracao de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Credenciais do usuario
DB_USER = "postgres"
DB_PASSWORD = "P$inUca01"

# Parametros de conexao com o banco de dados
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "db_borbaf",
    "user": DB_USER,
    "password": DB_PASSWORD,
}


def criar_conexao(config):
    # Cria e retorna uma conexao com o banco de dados PostgreSQL.
    # Em caso de falha, registra o erro e retorna None.
    if psycopg2 is None:
        logger.error("Biblioteca psycopg2 nao esta instalada.")
        return None
    try:
        conexao = psycopg2.connect(**config)
        logger.info("Conexao com o banco de dados estabelecida com sucesso.")
        return conexao
    except OperationalError as erro:
        logger.error("Erro ao conectar ao banco de dados: %s", erro)
        return None


def fechar_conexao(conexao):
    # Fecha a conexao com o banco de dados se ela estiver aberta.
    if conexao is not None:
        conexao.close()
        logger.info("Conexao com o banco de dados fechada.")


def executar_consulta(conexao, sql, parametros=None):
    # Executa uma consulta SQL e retorna os registros encontrados.
    # Retorna None em caso de erro.
    if conexao is None:
        logger.error("Conexao invalida. Nao foi possivel executar a consulta.")
        return None
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, parametros or ())
            registros = cursor.fetchall()
            logger.info("Consulta executada com sucesso. Registros: %d", len(registros))
            return registros
    except Exception as erro:
        logger.error("Erro ao executar consulta: %s", erro)
        return None


def main():
    # Funcao principal do programa.
    # Estabelece a conexao, executa uma consulta de teste e encerra.
    logger.info("Iniciando aplicacao main.py")
    logger.info("Usuario de banco configurado: %s", DB_USER)

    conexao = criar_conexao(DB_CONFIG)
    if conexao is None:
        logger.error("Nao foi possivel iniciar a aplicacao sem conexao com o banco.")
        sys.exit(1)

    try:
        resultado = executar_consulta(conexao, "SELECT current_user;")
        if resultado:
            logger.info("Usuario conectado no banco: %s", resultado[0][0])
        else:
            logger.warning("Nenhum resultado retornado pela consulta de teste.")
    finally:
        fechar_conexao(conexao)

    logger.info("Aplicacao finalizada com sucesso.")


if __name__ == "__main__":
    main()