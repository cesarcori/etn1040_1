from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from proyecto.decorators import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def lista(request):
    grupo = request.user.groups.get().name
    context = {'grupo':grupo,}
    return render(request, 'actividades/lista.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante','director','administrador'])
def historial(request, id_equipo):
    grupo = request.user.groups.get().name
    equipo = get_object_or_404(Equipo, id=id_equipo)
    actividades = ActividadHistorial.objects.filter(equipo=equipo).order_by('fecha_creacion')
    context = {'grupo':grupo,
            'actividades':actividades}
    return render(request, 'actividades/historial.html', context)

