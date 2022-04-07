from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save, m2m_changed
from django.dispatch import receiver

from .models import DatosEstudiante, Equipo, DatosDirector
from actividades.models import AvisoActividad

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

@receiver(m2m_changed, sender=DatosEstudiante.actividad.through)
def cambio_actividad(sender, action, instance, **kwargs):
    """Cuando se aumenta un valor en actividades del estudiante enviará
    un aviso."""
    if action == "post_add":
        print(f"*********** aviso agregado *******")
        if instance.equipo.tribunales.all().count() == 2:
            lista_usuarios = [
                instance.equipo.docente.usuario, 
                DatosDirector.objects.all()[0].usuario,
                instance.equipo.tutor.usuario, 
                instance.equipo.tribunales.all()[0].usuario,
                instance.equipo.tribunales.all()[1].usuario,
            ]
        elif instance.equipo.tutor:
            lista_usuarios = [
                instance.equipo.docente.usuario, 
                DatosDirector.objects.all()[0].usuario,
                instance.equipo.tutor.usuario, 
            ]
        else : 
            lista_usuarios = [
                instance.equipo.docente.usuario, 
                DatosDirector.objects.all()[0].usuario,
            ]
        actividad_agregada = instance.actividad.last()
        # existe relacion en base de datos revisar en cada usuario
        for usuario in lista_usuarios:
            aviso = AvisoActividad.objects.filter(usuario=usuario, equipo=instance.equipo)
            if aviso.exists():
                aviso[0].actividades.add(actividad_agregada)
            else:
                AvisoActividad.objects.create(
                    usuario = usuario,
                    equipo = instance.equipo,
                )
                aviso = AvisoActividad.objects.filter(usuario=usuario, equipo=instance.equipo)
                aviso[0].actividades.add(actividad_agregada)

