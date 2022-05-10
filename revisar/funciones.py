
def nota_max(cantidad_presentaciones):
    """
        Sigue la siguiente logica, segun reglamento.
        Informe 1. max 7
        Informe 2. max 7.5
        Informe 3. max 7.5
        Informe 4. max 5
        Informe 5. max 5
    """
    if cantidad_presentaciones < 5:
        dicc_return = {1:7, 2:7.5, 3:7.5, 4:5, 5:5}
        maximo = dicc_return[cantidad_presentaciones]
    else:
        maximo = 5
    return maximo
