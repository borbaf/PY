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
