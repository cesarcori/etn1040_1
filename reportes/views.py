from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from proyecto.decorators import unauthenticated_user, allowed_users, admin_only
from proyecto.models import DatosEstudiante

from .formularios import *
from .reportes import *
from .cartas import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director','tribunal'])
def cartaTutorAcepto(request, pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    reporte_tutor_acepto(buffer, estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_tutor_acepto.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director','tribunal'])
def formularioAceptacion(request,pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    generarformularioAceptacion(buffer,estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_aceptacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor',])
def reporteIndicacionesTutor(request, pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    http_host = request.META.get('HTTP_HOST')
    generarReporteIndicacionTutor(buffer, estudiante, http_host)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte_indicacion.pdf')
