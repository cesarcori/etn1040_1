#!/usr/bin/env python3 
# from fpdf import FPDF
# import libreriaCartas  
# from .libreriaCartas import *
from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import ActividadesCronograma, Equipo, RegistroPerfil, DatosDocente
from actividades.funciones import progress
from random import choice

# def infoCronograma(pk, estudiante):
    # equipo = get_object_or_404(Equipo, id=pk)
    # cronograma_existe = ActividadesCronograma.objects.filter(equipo=equipo).exists()
    # progreso = progress(estudiante)
    # # mensaje_limite = 'Aún tienes tiempo para elaborar el sistema'
    # mensaje_limite = ''
    # if cronograma_existe:
        # cronograma = ActividadesCronograma.objects.filter(usuario=estudiante)
            # # fecha de registro del cronograma o fecha de registro del proyecto
        # fecha = RegistroPerfil.objects.get(usuario=estudiante).fecha_creacion
            # # fecha limite sistema 2 años y medio
        # # prueba modificar el 0 del delta para eliminar al usuario
        # fecha = fecha.astimezone().date()#-timedelta(0)
        # fecha_limite_sistema = fecha+ timedelta(365*2.5)
        # dia_restante_sistema = fecha_limite_sistema - date.today()
        # dia_restante_sistema = dia_restante_sistema.days
        # # fecha transcurrida desde el inicio
        # dias_transcurridos = date.today() - fecha
        # dias_transcurridos = dias_transcurridos + timedelta(0)
        # # dias a semanas:
        # semanas = dias_transcurridos.days // 7# - 1
        # num_semana = dias_transcurridos.days // 7 + 1
        # dias = dias_transcurridos.days % 7
        # dias_transcurridos = dias_transcurridos.days# - 7
        # # duracion del proyecto
        # max_semana = range(1,1+max([n.semana_final for n in cronograma]))
        # semana_total = len(max_semana)
        # dia_total = 7*semana_total
        # # fecha limite cronograma
        # fecha_limite_crono = fecha + timedelta(dia_total)
        # dia_restante_crono = fecha_limite_crono - date.today()
        # dia_restante_crono = dia_restante_crono.days
        # # fecha limite sistema 2 años y medio
        # fecha_limite_sistema = fecha + timedelta(365*2.5)
        # dia_restante_sistema = fecha_limite_sistema - date.today()
        # dia_restante_sistema= dia_restante_sistema.days
        # # porcentaje
        # por_dia_crono = (dia_restante_crono* 100) / dia_total
        # por_dia_sistema = dia_restante_sistema* 100 / (365*2.5)
        # por_dia_crono = str(por_dia_crono)
        # por_dia_sistema = str(por_dia_sistema)

        # dia_retrazo = dia_restante_crono * -1
        # por_dia_retrazo = ( dia_restante_crono *-1* 100)/(365*2.5-dia_total) 
        # por_dia_retrazo= str(por_dia_retrazo)

        # if num_semana <= semana_total:
            # limite_cronograma = False
        # else:
            # actividades = []
            # limite_cronograma = True
        # # ********** casos de eliminacion del estudiante
        # # pasa 2 años y medio
        # if dia_restante_sistema <= -1 and progreso.nivel < 100:
            # # estudiante.usuario.delete()
            # print('Se jodio')
            # mensaje_limite = 'El estudiante fue eliminado del sistema por pasar los 2 años sin concluir el proyecto'
            # return (mensaje_limite)
        # # En caso de conclusion de proyecto 
        # if progreso.nivel >= 100:
            # fecha_100 = progreso.fecha_creacion
            # fecha_eliminar = fecha_100 + timedelta(100)
            # if fecha_eliminar.date() < date.today():
                # # estudiante.usuario.delete()
                # print('cuenta eliminada')
            # mensaje_limite = 'Concluiste con éxito el Proyecto de Grado, en 6 meses se eliminará tu cuenta'
            # dia_restante_crono = ''
            # dia_restante_sistema = ''
            # dia_retrazo = ''
            # semana_total = ''
            # por_dia_crono = ''
            # por_dia_sistema = ''
            # por_dia_retrazo = ''
            # limite_cronograma = ''
        # # caso de reglamento sanabria, no conclucion de perfil
        # if not estudiante.registroperfil:
            # fecha_ingreso = estudiante.fecha_inscripcion.date()
        # # se establese fecha limite del semestre de fin de septiembre y fin de marzo
            # if fecha_ingreso.month < 6: 
                # fecha_limite = date(fecha_ingreso.year,9,30)
            # else:
                # fecha_limite = date(fecha_ingreso.year+1,3,30)
            # if fecha_limite < date.today():
                # # estudiante.usuario.delete()
                # print('cuenta eliminada')
                # print('Se jodio')
                # mensaje_limite = 'El estudiante fue eliminado del sistema por no aprobar el perfil en el semestre inscrito'
                # return (mensaje_limite)
    # else:
        # dia_restante_crono = ''
        # dia_restante_sistema = ''
        # dia_retrazo = ''
        # semana_total = ''
        # por_dia_crono = ''
        # por_dia_sistema = ''
        # por_dia_retrazo = ''
        # limite_cronograma = ''
        # mensaje_limite = ''
    # context = {
                # 'dia_restante_crono':dia_restante_crono,
                # 'dia_restante_sistema':dia_restante_sistema,
                # 'dia_retrazo':dia_retrazo,
                # 'semana_total':semana_total,
                # 'por_dia_crono':por_dia_crono,
                # 'por_dia_sistema':por_dia_sistema,
                # 'por_dia_retrazo':por_dia_retrazo,
                # 'limite_cronograma':limite_cronograma,
                # 'cronograma_existe':cronograma_existe,
                # 'estudiante':estudiante,
            # 'dia_restante_sistema':dia_restante_sistema,
            # 'mensaje_limite':mensaje_limite}
    # return context

def sorteoDocente(estudiante):
    ''' Lo que realiza el algoritmo es:
        1: Encontrar docentes de la mencion del estudiante
        2: Encontrar los docentes con menor cantidad de estudiantes
        3: Sortear entre los que quienen un menor cantidad de estudiantes.'''
    mencion_estudiante = estudiante.mencion
    docentes_mencion = DatosDocente.objects.filter(mencion=mencion_estudiante)
    # diccionario, docente-numero de estudiantes
    docente_numEst = {}
    for docente in docentes_mencion:
        docente_numEst[docente] = docente.datosestudiante_set.count()
    # ordenando diccionario por valor, de menor a mayor
    sort_docente_numEst = sorted(docente_numEst.items(), key=lambda x:x[1])
    # extraer los menores:
    numero_menor_estudiantes = sort_docente_numEst[0][1]
    docentes_menor_estudiantes = []
    for doc_numEst in sort_docente_numEst:
        if doc_numEst[1] == numero_menor_estudiantes:
            docentes_menor_estudiantes.append(doc_numEst[0])
    docente_asignado = choice(docentes_menor_estudiantes)
    return docente_asignado

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

# email de activacion
def email_activacion(request, user, to_email):
    current_site = get_current_site(request)
    mail_subject = 'Activa tu cuenta.'
    message = render_to_string('proyecto/acc_activate_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()

# verificar que no haya ingreso a otros estudiantes por url id
# hacer para docente, tutor, tribunal.
# existe_est = request.user.datosdocente.datosestudiante_set.filter(id=pk_est).exists()
# if not existe_est:
    # return redirect('error')