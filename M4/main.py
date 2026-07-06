# ============================================================================
# Arquivo: main.py
# ============================================================================
#"""Arquivo principal que integra todas as operações de banco de dados.

#Este script demonstra o uso dos módulos de conexão, criação de tabela,
#inserção, seleção e atualização no PostgreSQL.
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