from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from .models import DatosEstudiante, Equipo

@receiver(post_save, sender=DatosEstudiante)
def crear_equipo(sender, instance, created, **kwargs):
    """Al momento de crear un estudiante se creara su grupo correspondiente"""
    if created:
        texto = f"{instance} - {instance.correo}"
        equipo = Equipo.objects.create(nombre=texto, cantidad=1, docente=instance.grupo_doc)
        instance.equipo = equipo
        instance.save()

@receiver(pre_delete, sender=Equipo)
def eliminar_equipo(sender, instance, **kwargs):
    """Al eliminar un equipo se eliminaran a todos sus estudiantes 
    relacionados con este"""
    estudiantes = instance.datosestudiante_set.all()
    for estudiante in estudiantes:
        estudiante.delete()

@receiver(post_save, sender=DatosEstudiante)
def cambio_docente(sender, instance, created, **kwargs):
    """Cuando se cambia el docente del estudiante, el docente del grupo
    tambien se actualizara."""
    if not created:
        instance.equipo.docente = instance.grupo_doc
        instance.equipo.save()

# @receiver(pre_delete, sender=NotaTribunal)
# def eliminar_nota(sender, instance, **kwargs):
    # """ Al eliminar la nota del tribunal, se reestablece las notas anteriores """
    # estudiantes = instance.datosestudiante_set.all()
    # for estudiante in estudiantes:
        # estudiante.delete()
