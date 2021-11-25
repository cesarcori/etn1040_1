from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from proyecto.decorators import *

from .forms import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def index(request):
    context = {}
    return render(request, 'mensaje/index.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def par(request):
    form = MensajeParForm
    context = {'form':form}
    return render(request, 'mensaje/mensaje.html', context)

@login_required(login_url='login')
def enviar2(request, pk_doc_tut_est):
    grupo = request.user.groups.get().name
    usuario = request.user
    id_user = request.user.id.__str__()
    id_link = pk_doc_tut_est.__str__()
    usuario_link = User.objects.get(id=id_link)
    if request.method == "POST":
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensajes = form
            mensaje= form.cleaned_data.get('texto')
            # guardando mensaje
            if grupo == 'tutor':
                nombre_sala = id_user + id_link
            elif grupo == 'estudiante':
                nombre_sala = id_link + id_user
            elif grupo == 'docente':
                nombre_sala = id_user + id_link
            sala = Sala.objects.get(nombre_sala=nombre_sala)
            guardar_mensaje = MensajeSala.objects.create(usuario=usuario, texto=mensaje, sala=sala)
            context = {'grupo': grupo,'form':form}
            return redirect('mensaje_personal', pk_doc_tut_est=pk_doc_tut_est)
    else:
        form = MensajeForm()
        if grupo == 'estudiante':
            nombre_sala = id_link + id_user
        elif grupo == 'tutor':
            nombre_sala = id_user + id_link
        elif grupo == 'docente':
            nombre_sala = id_user + id_link
        sala = Sala.objects.get(nombre_sala=nombre_sala)
        mensajes = sala.mensajesala_set.all().order_by('-fecha_creacion')
        context = {'grupo':grupo,'mensajes':mensajes,
                'form':form,'usuario_link':usuario_link}
        return render(request, 'proyecto/mensaje_personal.html', context)
