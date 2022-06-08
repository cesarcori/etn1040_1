from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

from .funciones import *

@receiver(post_save, sender=SalaDocumentoDoc)
def CrearValoresIniciales(sender, instance, created, **kwargs):
    """Al momento de crear la SalaDocumentoDoc se creará valores 
    predeterminados"""
    tipo = instance.tipo
    usuario = instance.revisor
    grupo = instance.grupo_revisor.__str__()

    if created:
        if grupo=='docente' or grupo=='tutor':
            configuracion, created = ConfiguracionSala.objects.get_or_create(usuario=usuario)
            predeterminado = configuracion.is_predeterminado
            if tipo == 'perfil':
                pass

            elif tipo == 'proyecto' and predeterminado:
                crearSalasPredeterminadas(RevisarDocPredeterminado.objects.filter(tipo="proyecto"), instance)

            elif tipo == 'proyecto' and not predeterminado:
                crearSalasPersonalizado(RevisarDocPersonalizado.objects.filter(tipo="proyecto", usuario=usuario), instance)

            elif tipo == 'tribunal':
                pass

