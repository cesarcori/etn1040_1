from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SalaRevisarApp, NotaSalaRevisarApp

@receiver(post_save, sender=SalaRevisarApp)
def CrearNota(sender, instance, created, **kwargs):
    """Al momento de crear un estudiante se creara su grupo correspondiente"""
    revisor = instance.sala_documento.revisor
    grupo = instance.sala_documento.grupo_revisor.name
    tipo = instance.sala_documento.tipo
    if grupo == 'docente' and tipo == 'proyecto':
        if created:
            NotaSalaRevisarApp.objects.create(revisor=revisor, sala=instance)
