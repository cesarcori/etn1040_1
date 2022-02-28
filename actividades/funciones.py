from datetime import date, timedelta
from django.http import HttpResponse
from django.http import FileResponse
from .models import Actividad
from proyecto.models import ActividadesCronograma, Equipo, RegistroPerfil

def progress(estudiante):

    actividades = Actividad.objects.all()
    actividades_estudiante = estudiante.actividad.all()
    suma_valores = 0
    for actividad in actividades:
        suma_valores += actividad.valor
    porcentaje_por_unidad = 100/suma_valores
    suma_valores_estudiante = 0
    for actividad in actividades_estudiante:
        suma_valores_estudiante += actividad.valor
    progreso_sobre_100 = int(suma_valores_estudiante * porcentaje_por_unidad)
    return progreso_sobre_100

def agregarActividadEstudiante(texto_actividad, estudiante):

    actividad = Actividad.objects.get(nombre=texto_actividad)
    estudiante.actividad.add(actividad)
    estudiante.save()

def agregarActividadEquipo(texto_actividad, equipo):

    estudiantes = equipo.datosestudiante_set.all()
    for estudiante in estudiantes:
        actividad = Actividad.objects.get(nombre=texto_actividad)
        estudiante.actividad.add(actividad)
        estudiante.save()

def actividadRealizadaEstudiante(texto_actividad, estudiante):

    hecho = estudiante.actividad.filter(nombre=texto_actividad).exists()
    return hecho

def pasosRealizados(estudiante):

    pasos = {1:2, 2:3, 3:7, 4:13, 5:18, 6:29}
    cantidad_actividades = estudiante.actividad.all().count()
    pasos_realizados = []
    # print(cantidad_actividades)

    for paso, actividad in pasos.items():
        if cantidad_actividades >= actividad:
            pasos_realizados.append(paso)
    # print(pasos_realizados)

    return pasos_realizados

def informarCronograma(pk):
    
    equipo = Equipo.objects.get(id=pk)
    cronograma_existe = ActividadesCronograma.objects.filter(equipo=equipo).exists()
    estudiante = equipo.datosestudiante_set.first()
    progreso = progress(estudiante)
    # mensaje_limite = 'Aún tienes tiempo para elaborar el sistema'
    mensaje_limite = ''
    if cronograma_existe:
        cronograma = ActividadesCronograma.objects.filter(equipo=estudiante.equipo)
            # fecha de registro del cronograma o fecha de registro del proyecto
        fecha = RegistroPerfil.objects.get(equipo=estudiante.equipo).fecha_creacion
            # fecha limite sistema 2 años y medio
        # prueba modificar el 0 del delta para eliminar al usuario
        fecha = fecha.astimezone().date()#-timedelta(0)
        fecha_limite_sistema = fecha+ timedelta(365*2.5)
        dia_restante_sistema = fecha_limite_sistema - date.today()
        dia_restante_sistema = dia_restante_sistema.days
        # fecha transcurrida desde el inicio
        dias_transcurridos = date.today() - fecha
        dias_transcurridos = dias_transcurridos + timedelta(0)
        # dias a semanas:
        semanas = dias_transcurridos.days // 7# - 1
        num_semana = dias_transcurridos.days // 7 + 1
        dias = dias_transcurridos.days % 7
        dias_transcurridos = dias_transcurridos.days# - 7
        # duracion del proyecto
        max_semana = range(1,1+max([n.semana_final for n in cronograma]))
        semana_total = len(max_semana)
        dia_total = 7*semana_total
        # fecha limite cronograma
        fecha_limite_crono = fecha + timedelta(dia_total)
        dia_restante_crono = fecha_limite_crono - date.today()
        dia_restante_crono = dia_restante_crono.days
        # fecha limite sistema 2 años y medio
        fecha_limite_sistema = fecha + timedelta(365*2.5)
        dia_restante_sistema = fecha_limite_sistema - date.today()
        dia_restante_sistema= dia_restante_sistema.days
        # porcentaje
        por_dia_crono = (dia_restante_crono* 100) / dia_total
        por_dia_sistema = dia_restante_sistema* 100 / (365*2.5)
        por_dia_crono = str(por_dia_crono)
        por_dia_sistema = str(por_dia_sistema)

        dia_retrazo = dia_restante_crono * -1
        por_dia_retrazo = ( dia_restante_crono *-1* 100)/(365*2.5-dia_total) 
        por_dia_retrazo= str(por_dia_retrazo)

        if num_semana <= semana_total:
            limite_cronograma = False
        else:
            actividades = []
            limite_cronograma = True
        # ********** casos de eliminacion del estudiante
        # pasa 2 años y medio
        if dia_restante_sistema <= -1 and progreso.nivel < 100:
            # estudiante.usuario.delete()
            print('Se jodio')
            mensaje_limite = 'El estudiante fue eliminado del sistema por pasar los 2 años sin concluir el proyecto'
            return (mensaje_limite)
        # En caso de conclusion de proyecto 
        if progress(estudiante) >= 100:
            fecha_100 = equipo.fecha_conclusion
            fecha_eliminar = fecha_100 + timedelta(180)
            if fecha_eliminar.date() < date.today():
                # estudiante.usuario.delete()
                print('cuenta eliminada')
            mensaje_limite = 'Concluiste con éxito el Proyecto de Grado, en 6 meses se eliminará tu cuenta'
            dia_restante_crono = ''
            dia_restante_sistema = ''
            dia_retrazo = ''
            semana_total = ''
            por_dia_crono = ''
            por_dia_sistema = ''
            por_dia_retrazo = ''
            limite_cronograma = ''
        # caso de reglamento sanabria, no conclusion de perfil
        if not estudiante.equipo.registroperfil:
            fecha_ingreso = estudiante.fecha_inscripcion.date()
        # se establese fecha limite del semestre de fin de septiembre y fin de marzo
            if fecha_ingreso.month < 6: 
                fecha_limite = date(fecha_ingreso.year,9,30)
            else:
                fecha_limite = date(fecha_ingreso.year+1,3,30)
            if fecha_limite < date.today():
                # estudiante.usuario.delete()
                print('cuenta eliminada')
                print('Se jodio')
                mensaje_limite = 'El estudiante fue eliminado del sistema por no aprobar el perfil en el semestre inscrito'
                return (mensaje_limite)
    else:
        dia_restante_crono = ''
        dia_restante_sistema = ''
        dia_retrazo = ''
        semana_total = ''
        por_dia_crono = ''
        por_dia_sistema = ''
        por_dia_retrazo = ''
        limite_cronograma = ''
        mensaje_limite = ''
    context = {
        'dia_restante_crono':dia_restante_crono,
        'dia_restante_sistema':dia_restante_sistema,
        'dia_retrazo':dia_retrazo,
        'semana_total':semana_total,
        'por_dia_crono':por_dia_crono,
        'por_dia_sistema':por_dia_sistema,
        'por_dia_retrazo':por_dia_retrazo,
        'limite_cronograma':limite_cronograma,
        'cronograma_existe':cronograma_existe,
        'estudiante':estudiante,
        'dia_restante_sistema':dia_restante_sistema,
        'mensaje_limite':mensaje_limite}
    return context

