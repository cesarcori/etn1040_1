from .models import *

def isVisto(de, para):
    """ de: user, para: user """
    # aviso del estudiante
    canal, created = CanalPar.objects.get_or_create(de=de, para=para)
    is_visto_lista = [n.is_visto for n in canal.mensajepar_set.all()]
    if is_visto_lista:
        is_visto = is_visto_lista[-1]
    else:
        is_visto = True

    return is_visto
