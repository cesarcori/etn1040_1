from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SalaDocumentoDoc, NotaSalaRevisarDoc, SalaRevisarDoc, RevisarDocPredeterminado
from .funciones import *

@receiver(post_save, sender=SalaRevisarDoc)
def CrearNota(sender, instance, created, **kwargs):
    """Al momento de crear un estudiante se creara su grupo correspondiente"""
    revisor = instance.sala_documento.revisor
    grupo = instance.sala_documento.grupo_revisor.name
    tipo = instance.sala_documento.tipo
    if grupo == 'docente' and tipo == 'proyecto':
        if created:
            NotaSalaRevisarDoc.objects.create(revisor=revisor, sala=instance)

@receiver(post_save, sender=SalaDocumentoDoc)
def CrearValoresIniciales(sender, instance, created, **kwargs):
    """Al momento de crear la SalaDocumentoDoc se creará valores 
    predeterminados"""
    tipo = instance.tipo
    predeterminado = instance.is_predeterminado

    if created:
        if tipo == 'perfil':
            pass

        elif tipo == 'proyecto' and predeterminado:
            crearSalasPredeterminadas(RevisarDocPredeterminado.objects.filter(tipo="proyecto"), instance)

        elif tipo == 'proyecto' and not predeterminado:
            crearSalasPredeterminadas(RevisarDocPredeterminado.objects.filter(tipo="proyecto"), instance)

        elif tipo == 'tribunal':
            pass

