from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from proyecto.decorators import *
from .forms import *
from actividades.funciones import *
from proyecto.models import RegistroPerfil, ProyectoDeGrado
from .funciones import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def revisarDocumentoEstudiante(request, documento, id_revisor):
    usuario = request.user
    grupo = usuario.groups.get().name
    revisor = User.objects.get(id=id_revisor)
    estudiante = request.user.datosestudiante
    grupo_revisor = revisor.groups.get()
    sala_doc, created = SalaDocumentoDoc.objects.get_or_create(revisor=revisor, grupo_revisor=grupo_revisor, equipo=estudiante.equipo, tipo=documento)
    salas_revisar = SalaRevisarDoc.objects.filter(sala_documento=sala_doc).order_by('-fecha_creacion')
    dicc_salas = {}
    for sala in salas_revisar:
        mensajes = MensajeRevisarDoc.objects.filter(sala=sala).exclude(usuario=usuario)
        no_visto = 0
        for mensaje in mensajes:
            if not mensaje.visto:
                no_visto += 1
        dicc_salas[sala] = no_visto
    suma = 0
    if grupo_revisor.name == 'docente' and sala_doc.tipo == 'proyecto' and salas_revisar.count() > 0:
        dicc_salas_no_visto_nota = {}
        no_visto_nota = []
        for sala, no_visto in dicc_salas.items():
            nota_sala = NotaSalaRevisarDoc.objects.get(revisor=revisor, sala=sala)
            no_visto_nota = [no_visto, nota_sala]
            dicc_salas_no_visto_nota[sala] = no_visto_nota
        dicc_salas = dicc_salas_no_visto_nota
        # nota promediada
        suma = 0
        for no_visto_nota in dicc_salas.values():
            suma += no_visto_nota[1].nota
    context = {
            'sala_doc':sala_doc,
            'dicc_salas':dicc_salas,
            'suma': suma,
            'grupo':grupo}
    return render(request, 'revisar_documentos/revisar_documento_estudiante.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal'])
def revisarDocumentoRevisor(request, documento, id_equipo):
    usuario = request.user
    grupo = usuario.groups.get().name
    revisor = usuario
    equipo = get_object_or_404(Equipo, id=id_equipo)
    grupo_revisor = revisor.groups.get()
    sala_doc, created = SalaDocumentoDoc.objects.get_or_create(revisor=revisor, grupo_revisor=grupo_revisor, equipo=equipo, tipo=documento)
    salas_revisar = SalaRevisarDoc.objects.filter(sala_documento=sala_doc).order_by('-fecha_creacion')
    dicc_salas = {}
    for sala in salas_revisar:
        mensajes = MensajeRevisarDoc.objects.filter(sala=sala).exclude(usuario=usuario)
        no_visto = 0
        for mensaje in mensajes:
            if not mensaje.visto:
                no_visto += 1
        dicc_salas[sala] = no_visto
    suma = 0
    if grupo_revisor.name == 'docente' and sala_doc.tipo == 'proyecto' and salas_revisar.count() > 0:
        dicc_salas_no_visto_nota = {}
        no_visto_nota = []
        for sala, no_visto in dicc_salas.items():
            nota_sala = NotaSalaRevisarDoc.objects.get(revisor=revisor, sala=sala)
            no_visto_nota = [no_visto, nota_sala]
            dicc_salas_no_visto_nota[sala] = no_visto_nota
        dicc_salas = dicc_salas_no_visto_nota
        # suma de notas
        suma = 0
        for no_visto_nota in dicc_salas.values():
            suma += no_visto_nota[1].nota

        # suma de nota max
        suma_max = 0
        for no_visto_nota in dicc_salas.values():
            suma_max += no_visto_nota[1].nota_max

    context = {
            'sala_doc':sala_doc,
            'dicc_salas':dicc_salas,
            'equipo':equipo,
            'suma': suma,
            'suma_max': suma_max,
            'grupo':grupo}

    return render(request, 'revisar_documentos/revisar_documento_revisor.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal'])
def modificarNotaMax(request, id_sala):
    grupo = request.user.groups.get().name
    revisor = request.user
    sala_revisar = get_object_or_404(SalaRevisarDoc, id=id_sala)
    nota_sala = NotaSalaRevisarDoc.objects.get(revisor=revisor, sala=sala_revisar)
    documento = nota_sala.sala.sala_documento.tipo
    equipo = nota_sala.sala.sala_documento.equipo

    salas_revisar = sala_revisar.sala_documento.salarevisardoc_set.all()
    notas_salas = [n.notasalarevisardoc_set.first() for n in salas_revisar]
    # suma de nota max
    suma_max = 0
    for nota in notas_salas:
        suma_max += nota.nota_max

    form = NotaMaxForm(instance=nota_sala)
    if request.method == 'POST':
        form = NotaMaxForm(request.POST, instance=nota_sala)
        if form.is_valid():
            form.save()
            return redirect('revisar_documentos:revisar_documento_revisor', documento=documento, id_equipo=equipo.id)
    context = {
            'nota_sala': nota_sala,
            'form': form,
            'suma': suma_max,
            'grupo': grupo,}

    return render(request, 'revisar_documentos/modificar_nota_max.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente', 'tutor', 'tribunal'])
def crearSalaRevisar(request, documento, id_sala_doc):
    sala_doc = SalaDocumentoDoc.objects.get(id=id_sala_doc)
    equipo = sala_doc.equipo
    primer_estudiante = equipo.datosestudiante_set.first()
    grupo = request.user.groups.get().name
    if sala_doc.tipo=='perfil':
        if not actividadRealizadaEstudiante('revisar perfil', primer_estudiante):
            agregarActividadEquipo('revisar perfil', equipo)
    elif sala_doc.tipo=='proyecto':
        if not actividadRealizadaEstudiante('revisar proyecto', primer_estudiante):
            agregarActividadEquipo('revisar proyecto', equipo)
    elif sala_doc.tipo=='tribunal':
        if not actividadRealizadaEstudiante('revisar tribunal', primer_estudiante):
            agregarActividadEquipo('revisar tribunal', equipo)
    form = SalaRevisarDocForm
    if request.method == 'POST':
        form = SalaRevisarDocForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.sala_documento = sala_doc
            # form.instance.creado_por = request.user.datosestudiante
            form.save()
            return redirect('revisar_documentos:revisar_documento_revisor', documento=sala_doc.tipo, id_equipo=equipo.id)
    context = {'form':form,
            'grupo': grupo}
    return render(request, 'revisar_documentos/crear_sala_revisar.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente', 'tutor', 'tribunal'])
def eliminarSalaRevisar(request, id_sala_rev):
    sala_rev = SalaRevisarDoc.objects.get(id=id_sala_rev)
    if not sala_rev.sala_documento.revisor == request.user:
        return HttpResponse('error')
    documento = sala_rev.sala_documento.tipo
    id_equipo = sala_rev.sala_documento.equipo.id
    grupo = request.user.groups.get().name
    if request.method == 'POST':
        sala_rev.delete()
        return redirect('revisar_documentos:revisar_documento_revisor', documento=documento, id_equipo=id_equipo)
    context = {
            'grupo': grupo}
    return render(request, 'revisar_documentos/eliminar_sala.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente'])
def calificarSalaRevision(request, pk):
    usuario = request.user
    grupo = usuario.groups.get().name
    nota_sala = get_object_or_404(NotaSalaRevisarDoc, id=pk, revisor=usuario)
    equipo = nota_sala.sala.sala_documento.equipo
    form = NotaSalaRevisarDocForm(instance=nota_sala)
    if request.method == 'POST':
        form = NotaSalaRevisarDocForm(request.POST, instance=nota_sala)
        if form.is_valid():
            form.save()
            return redirect('progreso_estudiante',pk=equipo.pk)
    sala_documento = SalaDocumentoDoc.objects.get(revisor=usuario, equipo=equipo, tipo='proyecto')
    numero_salas = sala_documento.salarevisardoc_set.count()
    nota_limite = nota_max(numero_salas)
    # suma de la nota
    salas_revisar = sala_documento.salarevisardoc_set.all()
    suma = 0
    for sala_revisar in salas_revisar:
        a = sala_revisar.notasalarevisardoc_set.first().nota
        suma += a
    # for no_visto_nota in dicc_salas.values():
        # suma += no_visto_nota[1].nota
    context = {
            'grupo':grupo,
            'nota_sala': nota_sala,
            'equipo': equipo,
            'form': form,
            'nota_limite': nota_limite,
            'suma': suma,
            }
    return render(request, 'revisar_documentos/calificar_sala_revision.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def mensajes(request, id_sala_rev):
    usuario = request.user
    grupo = usuario.groups.get()
    sala = SalaRevisarDoc.objects.get(id=id_sala_rev)
    ultima_sala = sala.sala_documento.salarevisardoc_set.all().last()
    is_ultima_sala = sala == ultima_sala
    form = MensajeRevisarDocForm
    if request.method == "POST":
        form= MensajeRevisarDocForm(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.sala = sala
            file.usuario = usuario
            file.save()
        return redirect('revisar_documentos:mensajes', id_sala_rev=id_sala_rev)
    mensajes = MensajeRevisarDoc.objects.filter(sala=sala).order_by('-fecha_creacion')
    mensajes_no_vistos = MensajeRevisarDoc.objects.filter(sala=sala, visto=False).exclude(usuario=usuario)
    for mensaje in mensajes_no_vistos:  
        mensaje.visto = True
        mensaje.save()
    context = {
            'form':form,
            'mensajes':mensajes,
            'sala':sala,
            'grupo':grupo.name,
            'is_ultima_sala':is_ultima_sala,
            }
    return render(request, 'revisar_documentos/mensajes.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal'])
def darVistoBueno(request, id_sala_doc):
    sala_doc = get_object_or_404(SalaDocumentoDoc, id=id_sala_doc)
    salas_revisar = SalaRevisarDoc.objects.filter(sala_documento=sala_doc)
    grupo_revisor = sala_doc.revisor.groups.get().name
    grupo = request.user.groups.get().name
    equipo = sala_doc.equipo
    if grupo_revisor == 'tribunal':
        if actividadRealizadaEstudiante("visto bueno tribunal 1", sala_doc.equipo.datosestudiante_set.first()):
            texto_actividad = f"visto bueno {sala_doc.tipo} 2"
        else:
            texto_actividad = f"visto bueno {sala_doc.tipo} 1"
    else:
        texto_actividad = f"visto bueno {sala_doc.tipo} {sala_doc.revisor.groups.get()}"

    if request.method == 'POST':
        if grupo_revisor == 'docente':
            if sala_doc.tipo == 'perfil':
                RegistroPerfil.objects.create(
                    equipo = sala_doc.equipo,
                    perfil = sala_doc.salarevisardoc_set.last().archivo_corregir,    
                )
            elif sala_doc.tipo == 'proyecto':
                notas = [s.notasalarevisardoc_set.first().nota for s in salas_revisar]
                suma = 0
                for nota in notas:
                    suma += nota
                proyecto, created = ProyectoDeGrado.objects.get_or_create(equipo=equipo)
                proyecto.nota_informes_trabajo = suma
                proyecto.archivo = sala_doc.salarevisardoc_set.last().archivo_corregir    
                proyecto.save()
                # ProyectoDeGrado.objects.create(
                    # equipo = sala_doc.equipo,
                    # archivo = sala_doc.salarevisardoc_set.last().archivo_corregir,    
                    # nota_informes_trabajo = suma
                # )
        sala_doc.visto_bueno = True
        sala_doc.save()
        agregarActividadEquipo(texto_actividad, sala_doc.equipo)
        return redirect('progreso_estudiante', pk=sala_doc.equipo.id)
    context = {'sala_doc':sala_doc,
            'grupo':grupo}
    return render(request, 'revisar_documentos/dar_visto_bueno.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente',])
def calificarSeminario(request, pk):
    grupo = request.user.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)
    proyecto, created = ProyectoDeGrado.objects.get_or_create(equipo=equipo)
    nota = proyecto.nota_expos_seminarios
    context = {
        'grupo':grupo,
        'nota': nota,
        'pk':pk,
    }
    return render(request, 'revisar_documentos/calificar_seminario.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente',])
def registrarParticipacionSeminario(request, pk):
    grupo = request.user.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)
    proyecto, created = ProyectoDeGrado.objects.get_or_create(equipo=equipo)
    nota = proyecto.nota_expos_seminarios
    if nota == 6:
        return redirect('revisar_documentos:calificar_seminario', pk=pk)
    if request.method == 'POST':
        proyecto.nota_expos_seminarios = nota + 2
        proyecto.save()
        return redirect('revisar_documentos:calificar_seminario', pk=pk)
    context = {
        'grupo':grupo,
        'nota': nota,
        'pk':pk,
    }
    return render(request, 'revisar/registrar_seminario.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente',])
def calificarCronograma(request, pk):
    grupo = request.user.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)
    proyecto, created = ProyectoDeGrado.objects.get_or_create(equipo=equipo)
    nota = proyecto.nota_cumplimiento_cronograma
    context = {
        'grupo':grupo,
        'nota': nota,
        'pk':pk,
    }
    return render(request, 'revisar_documentos/calificar_cronograma.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente',])
def registrarCumplimientoCronograma(request, pk):
    grupo = request.user.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)
    proyecto, created = ProyectoDeGrado.objects.get_or_create(equipo=equipo)
    nota = proyecto.nota_cumplimiento_cronograma
    if nota == 3:
        return redirect('revisar_documentos:calificar_cronograma', pk=pk)
    if request.method == 'POST':
        proyecto.nota_cumplimiento_cronograma = nota + 1
        proyecto.save()
        return redirect('revisar_documentos:calificar_cronograma', pk=pk)
    context = {
        'grupo':grupo,
        'nota': nota,
        'pk':pk,
    }
    return render(request, 'revisar_documentos/registrar_cronograma.html', context)
