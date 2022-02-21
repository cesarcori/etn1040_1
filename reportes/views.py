from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from proyecto.decorators import unauthenticated_user, allowed_users, admin_only
from proyecto.models import DatosEstudiante, Equipo

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
@allowed_users(allowed_roles=['estudiante','tutor',])
def reporteIndicacionesTutor(request, pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    http_host = request.META.get('HTTP_HOST')
    generarReporteIndicacionTutor(buffer, estudiante, http_host)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte_indicacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director','tribunal'])
def formularioAceptacion(request,pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    generarformularioAceptacion(buffer,estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_aceptacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante',])
def firmaTutorCapitulos(request, pk):
    buffer = io.BytesIO()
    # estudiante = DatosEstudiante.objects.get(id=pk)
    equipo = get_object_or_404(Equipo, id=pk)
    generarFirmaTutorCapitulos(buffer, equipo)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='capitulos.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
def cartaFinal(request, pk):
    buffer = io.BytesIO()
    equipo = Equipo.objects.get(id=pk)
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    generarCartaFinal(buffer, equipo)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_final.pdf')
