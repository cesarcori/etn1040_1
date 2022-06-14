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
from mensaje.funciones import isVisto

def comprobar(grupo, equipo, usuario):
    if grupo == "docente":
        if not equipo.docente.usuario == usuario:
            error = True
            return error
    elif grupo == "tutor":
        if not equipo.tutor.usuario == usuario:
            error = True
            return error
    elif grupo == "tribunal":
        if not equipo.tribunales.filter(usuario=usuario):
            error = True
            return error

def isVistoUsuarioEstudiante(usuario_request, usuario):
    # aviso del estudiante
    id_request = usuario_request.id.__str__()
    id_usuario = usuario.id.__str__()
    nombre_sala = id_usuario + id_request
    sala = Sala.objects.get(nombre_sala=nombre_sala)
    # print(sala)
    sala = Sala.objects.get(nombre_sala=nombre_sala).mensajesala_set.filter(usuario=usuario).last()
    if sala:
        is_visto = sala.is_visto
    else:
        is_visto = True
    return is_visto

def isVistoUsuario(usuario_request, usuario):
    # En caso que el usuario request sea el docente o tutor
    id_request = usuario_request.id.__str__()
    id_usuario = usuario.id.__str__()
    nombre_sala = id_usuario + id_request
    sala = Sala.objects.get(nombre_sala=nombre_sala).mensajesala_set.filter(usuario=usuario_request).last()
    if sala:
        is_visto = sala.is_visto
    else:
        is_visto = True
    return is_visto

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

