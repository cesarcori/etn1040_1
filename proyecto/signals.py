from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save, m2m_changed
from django.dispatch import receiver

from .models import DatosEstudiante, Equipo, DatosDirector
from actividades.models import AvisoActividad, ActividadHistorial, Actividad
from actividades.funciones import distanciaEntreActividades 

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

@receiver(post_delete, sender=DatosEstudiante)
def eliminar_estudiante(sender, instance, **kwargs):
    """Al eliminar un estudiante y el equipo es solo de uno 
    se eliminaran al equipo que pertenece, caso contrario no se realiza nada"""
    equipo = instance.equipo
    if instance.equipo.datosestudiante_set.count() < 2:
        equipo.delete()

@receiver(post_save, sender=DatosEstudiante)
def cambio_docente(sender, instance, created, **kwargs):
    """Cuando se cambia el docente del estudiante, el docente del grupo
    tambien se actualizara."""
    if not created:
        instance.equipo.docente = instance.grupo_doc
        instance.equipo.save()

@receiver(m2m_changed, sender=DatosEstudiante.actividad.through)
def cambio_actividad(sender, action, instance, pk_set, **kwargs):
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
        # actividad_agregada = instance.actividad.last()
        for pk in pk_set:
            actividad_agregada = Actividad.objects.get(id=pk)
        # existe relacion en base de datos revisar en cada usuario
        if pk_set:
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

            # agregar al historial.
            actividad_historial, created = ActividadHistorial.objects.get_or_create(equipo=instance.equipo, actividad=actividad_agregada)

@receiver(m2m_changed, sender=DatosEstudiante.actividad.through)
def agregar_actividad(sender, action, instance, pk_set, **kwargs):
    """Al agregar una actividad al estudiante se ejecutará"""
    if action == "post_add":
        for pk in pk_set:
            actividad_agregada = Actividad.objects.get(id=pk)
        # existe relacion en base de datos revisar en cada usuario
        if pk_set:
            actividad_historial, created = ActividadHistorial.objects.get_or_create(equipo=instance.equipo, actividad=actividad_agregada)
            # calcular el nivel_ie
            actividades = ActividadHistorial.objects.filter(equipo=instance.equipo).order_by('fecha_creacion')
            instance.nivel_ie = distanciaEntreActividades(actividades, instance.equipo)
            instance.save()

@receiver(m2m_changed, sender=DatosEstudiante.actividad.through)
def remover_actividad(sender, action, instance, pk_set, **kwargs):
    """Se removera tambien todas sus dependencias"""
    if action == "pre_remove":
        # quitando del historial de actividades del estudiante
        for pk in pk_set:
            actividad = Actividad.objects.get(id=pk)
            actividad_historial = ActividadHistorial.objects.get(equipo=instance.equipo, actividad=actividad)
            actividad_historial.delete()
            # recalcular el nivel_ie
            actividades = ActividadHistorial.objects.filter(equipo=instance.equipo).order_by('fecha_creacion')
            instance.nivel_ie = distanciaEntreActividades(actividades, instance.equipo)
            instance.save()

@receiver(post_save, sender=DatosEstudiante)
def cambio_nivel_ie(sender, instance, created, **kwargs):
    """Cuando el ie del estudiante se modifica tambien lo hace el ie 
    del equipo."""
    if not created:
        instance.equipo.nivel_ie = instance.nivel_ie
        instance.equipo.save()




