from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, allowed_users, admin_only

def bienvenidos(request):
    return render(request, 'proyecto/bienvenidos.html')

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'El Usuario o Contraseña es Incorrecto')
    context = {}
    return render(request, 'proyecto/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, 'proyecto/home.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente'])
def docente(request):
    grupo = 'docente'
    context = {'grupo': grupo}
    return render(request, 'proyecto/docente.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor'])
def tutor(request):
    grupo = 'tutor'
    context = {'grupo': grupo}
    return render(request, 'proyecto/tutor.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def estudiante(request):
    grupo = 'estudiante'
    context = {'grupo': grupo}
    return render(request, 'proyecto/estudiante.html', context)

def perfilUsuarios(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/estudiante.html', context)
    return render(request, 'proyecto/perfil.html')

def busquedaProyectos(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/busqueda.html', context)

def compartirTodos(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/compartir_todos.html', context)


