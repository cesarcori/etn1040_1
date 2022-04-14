from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q

from proyecto.decorators import *

from .forms import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def index(request):
    context = {}
    return render(request, 'mensaje/index.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def par2(request):
    form = MensajeParForm
    context = {'form':form}
    return render(request, 'mensaje/mensaje.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','estudiante'])
def par(request, pk_para):
    grupo = request.user.groups.get().name
    para_usuario = get_object_or_404(User, id=pk_para)
    usuario = request.user
    form = MensajeParForm()
    if request.method == "POST":
        form = MensajeParForm(request.POST)
        if form.is_valid():
            # mensajes = form
            texto = form.cleaned_data.get('texto')
            # guardando mensaje
            canal, created = CanalPar.objects.get_or_create(de=request.user, para=para_usuario)
            MensajePar.objects.create(usuario=usuario, texto=texto, canal=canal)
            # context = {'grupo': grupo,'form':form}
            return redirect('mensaje:enviar_mensaje_par', pk_para=pk_para)

    canal_de, created = CanalPar.objects.get_or_create(de=request.user, para=para_usuario)
    canal_para, created = CanalPar.objects.get_or_create(de=para_usuario, para=request.user)
    mensajes = MensajePar.objects.filter(Q(canal=canal_de) | Q(canal=canal_para)).order_by('-fecha_creacion')
    # vistos Trues
    for mensaje in canal_para.mensajepar_set.all():
        mensaje.is_visto = True;
        mensaje.save()

    context = {'grupo':grupo,'mensajes':mensajes,
            'form':form,'para_usuario':para_usuario}
    return render(request, 'mensaje/mensaje.html', context)
