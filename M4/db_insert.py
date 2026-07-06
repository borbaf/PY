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