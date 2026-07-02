def pure_increments(element, increment, limit):
    """
    Incrementa o elemento pelo incremento até atingir o limite.
    
    Args:
        element (int): O elemento inicial.
        increment (int): O valor a ser adicionado ao elemento.
        limit (int): O valor máximo que o elemento pode atingir.
    
    Returns:
        int: O valor final do elemento após os incrementos.
    """
    while element < limit:
        element += increment
    return element