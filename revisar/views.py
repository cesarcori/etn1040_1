from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from proyecto.decorators import *
from .forms import *
from actividades.funciones import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def index(request):
    form = SalaRevisarAppForm
    context = {'form':form}
    return render(request, 'revisar/index.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def revisarDocumento(request, documento, id_revisor):
    usuario = request.user
    grupo = usuario.groups.get()
    estudiante = request.user.datosestudiante
    revisor = User.objects.get(id=id_revisor)
    grupo_revisor = revisor.groups.get()
    sala_doc = SalaDocumentoApp.objects.get(revisor=revisor, grupo_revisor=grupo_revisor, equipo=estudiante.equipo, tipo=documento)
    salas_doc = SalaDocumentoApp.objects.filter(equipo=estudiante.equipo, tipo=documento)
    salas_revisar = SalaRevisarApp.objects.filter(sala_documento=sala_doc).order_by('-fecha_creacion')
    dicc_salas = {}
    for sala in salas_revisar:
        mensajes = MensajeRevisarApp.objects.filter(sala=sala).exclude(usuario=usuario)
        no_visto = 0
        for mensaje in mensajes:
            if not mensaje.visto:
                no_visto += 1
        dicc_salas[sala] = no_visto
    context = {
            'sala_doc':sala_doc,
            'dicc_salas':dicc_salas,
            'salas_doc': salas_doc,
            'grupo':grupo.name}
    return render(request, 'revisar/revisar_documento.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def crearSalaRevisar(request, documento, id_revisor, id_sala_doc):
    sala_doc = SalaDocumentoApp.objects.get(id=id_sala_doc)
    equipo = sala_doc.equipo
    primer_estudiante = equipo.datosestudiante_set.first()
    if sala_doc.tipo=='perfil':
        if not actividadRealizadaEstudiante('revisar perfil', primer_estudiante):
            agregarActividadEstudiante('revisar perfil', primer_estudiante)
    elif sala_doc.tipo=='proyecto':
        if not actividadRealizadaEstudiante('revisar proyecto', primer_estudiante):
            agregarActividadEstudiante('revisar proyecto', primer_estudiante)
    elif sala_doc.tipo=='tribunal':
        if not actividadRealizadaEstudiante('revisar tribunal', primer_estudiante):
            agregarActividadEstudiante('revisar tribunal', primer_estudiante)
    form = SalaRevisarAppForm
    if request.method == 'POST':
        form = SalaRevisarAppForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.sala_documento = sala_doc
            form.instance.creado_por = request.user.datosestudiante
            form.save()
            return redirect('revisar:revisar_documento', documento=sala_doc.tipo, id_revisor=sala_doc.revisor.id)
    context = {'form':form,}
    return render(request, 'revisar/crear_sala_revisar.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def mensajes(request, id_sala_rev):
    usuario = request.user
    grupo = usuario.groups.get()
    sala = SalaRevisarApp.objects.get(id=id_sala_rev)
    form = MensajeRevisarAppForm
    if request.method == "POST":
        form= MensajeRevisarAppForm(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.sala = sala
            file.usuario = usuario
            file.save()
        return redirect('revisar:mensajes', id_sala_rev=id_sala_rev)
    mensajes = MensajeRevisarApp.objects.filter(sala=sala).order_by('-fecha_creacion')
    mensajes_no_vistos = MensajeRevisarApp.objects.filter(sala=sala, visto=False).exclude(usuario=usuario)
    for mensaje in mensajes_no_vistos:  
        mensaje.visto = True
        mensaje.save()
    context = {
            'form':form,
            'mensajes':mensajes,
            'sala':sala,
            'grupo':grupo.name,
            }
    return render(request, 'revisar/mensajes.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal'])
def darVistoBueno(request, id_sala_doc):
    sala_doc = get_object_or_404(SalaDocumentoApp, id=id_sala_doc)
    texto_actividad = f"visto bueno {sala_doc.tipo} {sala_doc.revisor.groups.get()}"
    agregarActividadEquipo(texto_actividad, sala_doc.equipo)
    if request.method == 'POST':
        sala_doc.visto_bueno = True
        sala_doc.save()
        return redirect('progreso_estudiante', pk=sala_doc.equipo.id)
    context = {'sala_doc':sala_doc}
    return render(request, 'revisar/dar_visto_bueno.html', context)



