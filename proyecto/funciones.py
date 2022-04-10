#!/usr/bin/env python3 
# from fpdf import FPDF
# import libreriaCartas  
# from .libreriaCartas import *
from datetime import date, timedelta
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import ActividadesCronograma, Equipo, RegistroPerfil, DatosDocente, Sala
from actividades.funciones import progress
from random import choice
from actividades.models import AvisoActividad


def isVistoUsuarioEstudiante(usuario_request, usuario):
    # aviso del estudiante
    id_request = usuario_request.id.__str__()
    id_usuario = usuario.id.__str__()
    nombre_sala = id_usuario + id_request
    sala = Sala.objects.get(nombre_sala=nombre_sala).mensajesala_set.filter(usuario=usuario).last()
    if sala:
        is_visto = sala.is_visto
    else:
        is_visto = True
    return is_visto

def isVistoUsuario(usuario_request, usuario):
    # aviso del estudiante
    id_request = usuario_request.id.__str__()
    id_usuario = usuario.id.__str__()
    nombre_sala = id_usuario + id_request
    sala = Sala.objects.get(nombre_sala=nombre_sala).mensajesala_set.filter(usuario=usuario_request).last()
    if sala:
        is_visto = sala.is_visto
    else:
        is_visto = True
    return is_visto

def avisosEstudiantes(datos_est, usuario):
    avisos = AvisoActividad.objects.filter(usuario=usuario)
    datos_estudiantes = {}
    for dato_est in datos_est:
        aviso_estudiante = avisos.filter(equipo=dato_est.equipo)
        if aviso_estudiante.exists():
            lista_actividades = aviso_estudiante[0].actividades.all()
            if lista_actividades.count() != 0:
                nombre_actividades = [f"{n}: {a.nombre}" for n, a in enumerate(lista_actividades, 1)]
                mensaje = "\n".join(nombre_actividades)
            else:
                mensaje = "No realizó actividad nueva"
            datos_estudiantes[dato_est] = [aviso_estudiante[0].actividades.all().count(), mensaje,
                isVistoUsuario(dato_est.usuario, usuario)]
        else:
            datos_estudiantes[dato_est] = [0, "No tiene ninguna actividad", isVistoUsuario(dato_est.usuario, usuario)]
    orden_datos_estudiantes = dict(sorted(datos_estudiantes.items(), key=lambda cantidad: cantidad[1][0], reverse=True))
    return orden_datos_estudiantes

def avisosEquipos(equipos_multiple, usuario):
    avisos = AvisoActividad.objects.filter(usuario=usuario)
    datos_equipos= {}
    for equipo in equipos_multiple:
        aviso_equipo = avisos.filter(equipo=equipo)
        if aviso_equipo.exists():
            lista_actividades = aviso_equipo[0].actividades.all()
            if lista_actividades.count() != 0:
                nombre_actividades = [f"{n}: {a.nombre}" for n, a in enumerate(lista_actividades, 1)]
                mensaje = "\n".join(nombre_actividades)
            else:
                mensaje = "No realizó actividad nueva"
            datos_equipos[equipo] = [aviso_equipo[0].actividades.all().count(), mensaje]
        else:
            datos_equipos[equipo] = [0, "No tiene ninguna actividad"]
    orden_datos_equipos = dict(sorted(datos_equipos.items(), key=lambda cantidad: cantidad[1][0], reverse=True))
    return orden_datos_equipos

def marcarAvisosVistos(equipo, usuario):
    aviso = AvisoActividad.objects.filter(usuario=usuario, equipo=equipo)
    if aviso.exists():
        aviso[0].actividades.clear()

def mensajesAvisosLista(equipo, usuario):
    aviso = AvisoActividad.objects.filter(usuario=usuario, equipo=equipo)
    if aviso.exists():
        lista_actividades = aviso[0].actividades.all()
        # mensajes = [f"{n}: {a.nombre}" for n, a in enumerate(lista_actividades, 1)]
        mensajes = [f"{n.nombre}" for n in lista_actividades]
    else:
        mensajes = []
    return mensajes

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

