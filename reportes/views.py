from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from proyecto.decorators import unauthenticated_user, allowed_users, admin_only, permitir_paso1
from proyecto.models import DatosEstudiante

from .formularios import *
from .cartas import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director','tribunal'])
# @permitir_paso3()
def cartaTutorAcepto(request, pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    reporte_tutor_acepto(buffer, estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_tutor_acepto.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director','tribunal'])
def formAceptacion(request,id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    formulario1(buffer,estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_aceptacion.pdf')
