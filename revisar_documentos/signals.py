from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

from .funciones import *
from actividades.funciones import agregarActividadEquipo

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

@receiver(post_save, sender=SalaRevisarDoc)
def primeraSalaRevision(sender, instance, created, **kwargs):
    """Si es la primera sala revision creada por el revisor en un determinado
    documento, registrarlo como inicio de revision"""

    equipo = instance.sala_documento.equipo
    documento = instance.sala_documento.tipo
    sala_doc = instance.sala_documento
    grupo = sala_doc.grupo_revisor.name

    # ver si es la primera sala
    cantidad = sala_doc.salarevisardoc_set.count()
    if cantidad == 1:
        is_primera_sala = True
    else:
        is_primera_sala = False
    
    if created and is_primera_sala:
        if sala_doc.tipo=='tribunal':
            tribunales = equipo.tribunales.all()
            if sala_doc.revisor.datostribunal == tribunales[0]:
                numero = '1'
            else:
                numero = '2'
            agregarActividadEquipo('revisar tribunal ' + numero, equipo)
        else:
            agregarActividadEquipo('revisar ' + documento + ' ' + grupo, equipo)

@receiver(post_save, sender=SalaDocumentoDoc)
def cambioSalaDocumentoDoc(sender, instance, update_fields, **kwargs):
    """Al momento de crear la SalaDocumentoDoc se creará valores 
    predeterminados"""
    tipo = instance.tipo
    usuario = instance.revisor
    grupo = instance.grupo_revisor.__str__()
    if update_fields:
        if 'visto_bueno' in update_fields:
            print("Se cambio el visto bueno")
            print(update_fields)
            print(instance.visto_bueno)
