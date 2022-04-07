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
from actividades.models import AvisoActividad

def avisosEstudiantes(datos_est, usuario):
    avisos = AvisoActividad.objects.filter(usuario=usuario)
    datos_estudiantes = {}
    for dato_est in datos_est:
        aviso_estudiante = avisos.filter(equipo=dato_est.equipo)
        if aviso_estudiante.exists():
            lista_actividades = aviso_estudiante[0].actividades.all()
            if lista_actividades.count() != 0:
                nombre_actividades = [f"{n}: {a.nombre}" for n, a in enumerate(aviso_estudiante[0].actividades.all(), 1)]
                mensaje = "\n".join(nombre_actividades)
            else:
                mensaje = "No realizó actividad nueva"
            datos_estudiantes[dato_est] = [aviso_estudiante[0].actividades.all().count(), mensaje]
        else:
            datos_estudiantes[dato_est] = [0, "No tiene ninguna actividad"]
    orden_datos_estudiantes = dict(sorted(datos_estudiantes.items(), key=lambda cantidad: cantidad[1][0], reverse=True))
    return orden_datos_estudiantes

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

