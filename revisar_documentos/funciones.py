from .models import SalaRevisarDoc

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

def crearSalasPredeterminadas(query_set, sala_documento):
    """ Se crean las salas según consulta a base de datos RevisarDocPredeterminado
    en ahí se encuentra la lista con la cual se creará las salas."""
    for query in query_set:
        asunto = query.asunto
        detalle = query.detalle
        nota_max = query.nota_max
        SalaRevisarDoc.objects.create(
            sala_documento = sala_documento,
            asunto = asunto, 
            detalle = detalle,
            nota_max = nota_max,
        )
