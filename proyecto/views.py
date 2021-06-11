from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import *
from .models import *

def bienvenidos(request):
    return render(request, 'proyecto/bienvenidos.html')
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm
    usuarios = User.objects.all()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            correo = form.cleaned_data.get('email')
            nombre = form.cleaned_data.get('nombre')
            apellido = form.cleaned_data.get('apellido')
            carnet = form.cleaned_data.get('carnet')
            registro_uni = form.cleaned_data.get('registro_uni')
            celular = form.cleaned_data.get('celular')
            mencion = form.cleaned_data.get('mencion')
            if User.objects.filter(username=usuario).exists():
                messages.info(request, 
            'No se envió la solicitud, un estudiante ya usa este nombre de usuario')
            elif User.objects.filter(email=correo).exists():
                messages.info(request,
            'No se envió la solicitud, un estudiante ya usa este correo electrónico')
            elif SolicitudInvitado.objects.filter(usuario=usuario).exists():
                messages.info(request, 
            'No se envió la solicitud, un solicitante usa este mismo nombre de usuario')
            elif SolicitudInvitado.objects.filter(correo=correo).exists():
                messages.info(request, 
            'No se envió la solicitud, un solicitante usa este mismo correo electrónico')
            elif SolicitudInvitado.objects.filter(carnet=carnet).exists():
                messages.info(request, 
            'No se envió la solicitud, un solicitante usa este mismo número de carnet')
            elif SolicitudInvitado.objects.filter(registro_uni=registro_uni).exists():
                messages.info(request, 
            'No se envió la solicitud, un solicitante usa este mismo número de \
            registro universitario')
            else:
                SolicitudInvitado.objects.create(
                        usuario = usuario,
                        correo = correo,
                        nombre = nombre,
                        apellido = apellido,
                        carnet = carnet,
                        registro_uni = registro_uni,
                        celular = celular,
                        mencion = mencion,
                        )
                messages.success(request, 'La solicitud de envio con exito!!!')
    context = {'usuarios':usuarios, 'form':form}
    return render(request, 'proyecto/registro_estudiante.html', context)

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
    form = Habilitar
    grupo = 'administrador'
    solicitudes = SolicitudInvitado.objects.all()
    context = {'grupo': grupo, 'solicitudes':solicitudes,'form':form}
    return render(request, 'proyecto/home.html', context)

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

@login_required(login_url='login')
def perfilUsuarios(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/perfil.html', context)

@login_required(login_url='login')
def busquedaProyectos(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/busqueda.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor'])
def compartirTodos(request):
    grupo = request.user.groups.all()[0].name # es lo mismo que arriba
    context = {'grupo': grupo}
    return render(request, 'proyecto/compartir_todos.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','estudiante'])
def compartirPersonal(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/compartir_personal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','administrador'])
def enlaceEstudiante(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/enlace_estudiante.html', context)

@login_required(login_url='login')
@admin_only
def enlaceDocente(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/enlace_docente.html', context)

@login_required(login_url='login')
@admin_only
def registroEstudiante(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/registro_estudiante.html', context)

@login_required(login_url='login')
@admin_only
def listaEstudiantes(request):
    context = {}
    return render(request, 'proyecto/lista_estudiante.html', context)

@login_required(login_url='login')
@admin_only
def listaDocentes(request):
    context = {}
    return render(request, 'proyecto/lista_docente.html', context)
