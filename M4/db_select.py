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