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

