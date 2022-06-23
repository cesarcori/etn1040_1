from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from proyecto.decorators import *
from .forms import *
from actividades.funciones import *
from proyecto.models import RegistroPerfil, ProyectoDeGrado
from .funciones import *
from proyecto.funciones import comprobar

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','tribunal'])
def revisiones(request, pk):
    usuario = request.user
    grupo = usuario.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)

    if comprobar(grupo, equipo, usuario):
        return HttpResponse('error')

    salas_documentos = SalaDocumentoDoc.objects.filter(revisor=usuario, equipo=equipo)

    is_perfil_habilitado = isActividad(equipo, "imprimir carta tutoria")
    is_perfil_terminado = isActividad(equipo, "imprimir formulario")
    is_proyecto_terminado = isActividad(equipo, "nota docente proyecto")
    is_vb_proyecto_tutor = isActividad(equipo, "visto bueno proyecto tutor")
    is_vb_perfil_tutor = isActividad(equipo, "visto bueno perfil tutor")

    context = {
        'grupo': grupo,
        'equipo': equipo,
        'salas_documentos': salas_documentos,
        'is_perfil_habilitado': is_perfil_habilitado,
        'is_perfil_terminado': is_perfil_terminado,
        'is_proyecto_terminado': is_proyecto_terminado,
        'is_vb_proyecto_tutor': is_vb_proyecto_tutor,
        'is_vb_perfil_tutor': is_vb_perfil_tutor,
    }
    return render(request, 'revisar_documentos/revisiones.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor'])
def configurar(request, pk):
    revisor = request.user
    grupo = revisor.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)

    if grupo=='docente':
        docente = revisor.datosdocente
        if not Equipo.objects.filter(docente=docente):
            return HttpResponse('error')

    configuracion, created = ConfiguracionSala.objects.get_or_create(usuario=revisor)
    salas = RevisarDocPersonalizado.objects.filter(usuario=revisor).order_by('orden')
    salas_pre = RevisarDocPredeterminado.objects.all().order_by('orden')
    suma_max = 0
    for sala in salas:
        suma_max += sala.nota_max
    
    context = {
        'grupo': grupo,
        'revisor': revisor,
        'equipo': equipo,
        'salas': salas,
        'salas_pre': salas_pre,
        'configuracion': configuracion,
        'suma_max': suma_max
    }
    if grupo == 'docente':
        return render(request, 'revisar_documentos/configurar.html', context)
    else:
        return render(request, 'revisar_documentos/configurar_revisor.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente', 'tutor'])
def cambiarPredeterminado(request, pk):
    revisor = request.user
    grupo = revisor.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)
    configuracion = ConfiguracionSala.objects.get(usuario=revisor)

    if grupo=='docente':
        docente = revisor.datosdocente
        if not Equipo.objects.filter(docente=docente):
            return HttpResponse('error')

    if request.method == 'POST':
        if configuracion.is_predeterminado == False:
            configuracion.is_predeterminado = True
            configuracion.save()
        else:
            configuracion.is_predeterminado = False
            configuracion.save()
        return redirect('revisar_documentos:configurar', pk=equipo.id)
    
    context = {
        'grupo': grupo,
        'revisor': revisor,
        'equipo': equipo,
    }

    return render(request, 'revisar_documentos/cambiar_predeterminado.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','tribunal'])
def crearSalaPersonal(request, pk):
    revisor = request.user
    grupo = revisor.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)

    if grupo=='docente':
        docente = revisor.datosdocente
        if not Equipo.objects.filter(docente=docente):
            return HttpResponse('error')

    if grupo=='tutor':
        tutor = revisor.datostutor
        if not Equipo.objects.filter(tutor=tutor):
            return HttpResponse('error')

    if grupo=='docente':
        form = crearRevisarDocPersonalizadoForm()
    else:
        form = crearRevisarDocPersonalizadoRevisorForm()

    if request.method == 'POST':
        if grupo=='docente':
            form = crearRevisarDocPersonalizadoForm(request.POST)
        else:
            form = crearRevisarDocPersonalizadoRevisorForm(request.POST)
        if form.is_valid():
            form.instance.usuario = revisor
            form.instance.tipo = "proyecto"
            form.save()
            return redirect('revisar_documentos:configurar', pk=equipo.id)
    
    salas = RevisarDocPersonalizado.objects.filter(usuario=revisor, tipo='proyecto')
    suma_max = 0
    for sala in salas:
        suma_max += sala.nota_max

    context = {
        'grupo': grupo,
        'revisor': revisor,
        'equipo': equipo,
        'suma_max': suma_max,
        'form': form,
    }
    return render(request, 'revisar_documentos/crear_sala_personalizado.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','tribunal'])
def eliminarSalaPersonal(request, pk_equipo, pk):
    revisor = request.user
    grupo = revisor.groups.get().name
    sala = get_object_or_404(RevisarDocPersonalizado, id=pk)
    equipo = get_object_or_404(Equipo, id=pk_equipo)

    if not RevisarDocPersonalizado.objects.filter(usuario=revisor):
        return HttpResponse('error')

    if request.method == 'POST':
        sala.delete()
        return redirect('revisar_documentos:configurar', pk=equipo.id)
    
    context = {
        'grupo': grupo,
        'revisor': revisor,
        'equipo': equipo,
    }
    return render(request, 'revisar_documentos/eliminar_sala.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','tribunal'])
def modificarSalaPersonal(request, pk_equipo, pk):
    revisor = request.user
    grupo = revisor.groups.get().name
    sala = get_object_or_404(RevisarDocPersonalizado, id=pk)
    equipo = get_object_or_404(Equipo, id=pk_equipo)

    if not RevisarDocPersonalizado.objects.filter(usuario=revisor):
        return HttpResponse('error')

    if grupo=='docente':
        form = crearRevisarDocPersonalizadoForm(instance=sala)
    else:
        form = crearRevisarDocPersonalizadoRevisorForm(instance=sala)

    if request.method == 'POST':
        if grupo=='docente':
            form = crearRevisarDocPersonalizadoForm(request.POST, instance=sala)
        else:
            form = crearRevisarDocPersonalizadoRevisorForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
        return redirect('revisar_documentos:configurar', pk=equipo.id)

    salas = RevisarDocPersonalizado.objects.filter(usuario=revisor, tipo='proyecto')
    suma_max = 0
    for sala in salas:
        suma_max += sala.nota_max
    
    context = {
        'grupo': grupo,
        'revisor': revisor,
        'equipo': equipo,
        'suma_max': suma_max,
        'form': form,
    }
    return render(request, 'revisar_documentos/modificar_sala_personal.html', context)

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
        suma = 0
        for sala in salas_revisar:
            suma += sala.nota
    context = {
            'sala_doc':sala_doc,
            'dicc_salas':dicc_salas,
            'suma': suma,
            'grupo':grupo}
    return render(request, 'revisar_documentos/revisar_documento_estudiante.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal'])
def revisarDocumentoRevisor(request, documento, id_equipo):
    grupo = request.user.groups.get().name
    revisor = request.user
    equipo = get_object_or_404(Equipo, id=id_equipo)
    grupo_revisor = revisor.groups.get()

    if documento=='proyecto' and not isActividad(equipo, "imprimir formulario"): 
        return HttpResponse('error')
    if documento=='perfil' and not isActividad(equipo, "imprimir carta tutoria"):
        return HttpResponse('error')
    if documento=='proyecto' and grupo=="docente" and not isActividad(equipo, "visto bueno proyecto tutor"): 
        return HttpResponse('error')

    sala_doc, created = SalaDocumentoDoc.objects.get_or_create(revisor=revisor, grupo_revisor=grupo_revisor, equipo=equipo, tipo=documento)
    salas_revisar = SalaRevisarDoc.objects.filter(sala_documento=sala_doc).order_by('-fecha_creacion')
    dicc_salas = {}
    for sala in salas_revisar:
        mensajes = MensajeRevisarDoc.objects.filter(sala=sala).exclude(usuario=request.user)
        no_visto = 0
        for mensaje in mensajes:
            if not mensaje.visto:
                no_visto += 1
        dicc_salas[sala] = no_visto
    suma = 0
    suma_max = 0
    if grupo_revisor.name == 'docente' and sala_doc.tipo == 'proyecto' and salas_revisar.count() > 0:
        suma = 0
        for sala in salas_revisar:
            suma += sala.nota

        # suma de nota max
        suma_max = 0
        for sala in salas_revisar:
            suma_max += sala.nota_max

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
    if sala_revisar.is_calificado:
        return HttpResponse('error')
    documento = sala_revisar.sala_documento.tipo
    equipo = sala_revisar.sala_documento.equipo

    salas_revisar = sala_revisar.sala_documento.salarevisardoc_set.all()
    # suma de nota max
    suma_max = 0
    for sala in salas_revisar:
        suma_max += sala.nota_max

    form = NotaMaxForm(instance=sala_revisar)
    if request.method == 'POST':
        form = NotaMaxForm(request.POST, instance=sala_revisar)
        if form.is_valid():
            form.save()
            return redirect('revisar_documentos:revisar_documento_revisor', documento=documento, id_equipo=equipo.id)
    context = {
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
    salas_revisar = sala_doc.salarevisardoc_set.all()
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
            form.save()
            return redirect('revisar_documentos:revisar_documento_revisor', documento=sala_doc.tipo, id_equipo=equipo.id)
    suma_max = 0
    for sala in salas_revisar:
        suma_max += sala.nota_max

    context = {'form':form,
            'suma_max': suma_max,
            'grupo': grupo}
    return render(request, 'revisar_documentos/crear_sala_revisar.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente', 'tutor', 'tribunal'])
def crearSalaSinNota(request, documento, id_sala_doc):
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
    form = SalaRevisarDocSinNotaForm
    if request.method == 'POST':
        form = SalaRevisarDocSinNotaForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.sala_documento = sala_doc
            form.save()
            return redirect('revisar_documentos:revisar_documento_revisor', documento=sala_doc.tipo, id_equipo=equipo.id)

    context = {'form':form,
            'grupo': grupo}

    return render(request, 'revisar_documentos/crear_sala_sin_nota.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente', 'tutor', 'tribunal'])
def eliminarSalaRevisar(request, id_sala_rev):
    sala_rev = SalaRevisarDoc.objects.get(id=id_sala_rev)
    if not sala_rev.sala_documento.revisor == request.user:
        return HttpResponse('error')
    if sala_rev.is_calificado:
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
@allowed_users(allowed_roles=['docente', 'tutor', 'tribunal'])
def cerrarSalaRevisar(request, id_sala_rev):
    sala_rev = SalaRevisarDoc.objects.get(id=id_sala_rev)

    if not sala_rev.sala_documento.revisor == request.user:
        return HttpResponse('error')
    if sala_rev.is_calificado:
        return HttpResponse('error')

    documento = sala_rev.sala_documento.tipo
    id_equipo = sala_rev.sala_documento.equipo.id
    grupo = request.user.groups.get().name

    if request.method == 'POST':
        sala_rev.is_calificado = True
        sala_rev.save()
        return redirect('revisar_documentos:revisar_documento_revisor', documento=documento, id_equipo=id_equipo)

    context = {
        'grupo': grupo,
        'sala': sala_rev,
    }

    return render(request, 'revisar_documentos/cerrar_sala.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def subirDocumento(request, pk):
    sala_revisar = SalaRevisarDoc.objects.get(id=pk)
    estudiante = request.user.datosestudiante
    documento = sala_revisar.sala_documento.tipo
    revisor = sala_revisar.sala_documento.revisor
    equipo = estudiante.equipo
    if sala_revisar.sala_documento.equipo != equipo:
        return HttpResponse('error')
    grupo = request.user.groups.get().name
    form = SubirDocumentoForm(instance=sala_revisar)
    if request.method == 'POST':
        form = SubirDocumentoForm(request.POST, request.FILES, instance=sala_revisar)
        if form.is_valid():
            form.save()
            agregarAviso('revisar '+ documento, equipo, revisor)
            agregarActividadEquipo('revisar ' + documento, equipo)
            return redirect('revisar_documentos:revisar_documento_estudiante', documento=documento, id_revisor=revisor.id)
    context = {'form':form,
            'grupo': grupo}
    return render(request, 'revisar_documentos/subir_documento.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente'])
def calificarSalaRevision(request, pk):
    usuario = request.user
    grupo = usuario.groups.get().name
    sala_revisar = get_object_or_404(SalaRevisarDoc, id=pk)
    if sala_revisar.is_calificado:
        return HttpResponse('error')
    documento = sala_revisar.sala_documento
    equipo = documento.equipo
    equipo = sala_revisar.sala_documento.equipo
    form = NotaSalaRevisarDocForm(instance=sala_revisar)
    if request.method == 'POST':
        form = NotaSalaRevisarDocForm(request.POST, instance=sala_revisar)
        if form.is_valid():
            form.instance.is_calificado = True
            form.save()
            # return redirect('progreso_estudiante',pk=equipo.pk)
            return redirect('revisar_documentos:revisar_documento_revisor', documento=documento.tipo, id_equipo=equipo.id)
    sala_documento = SalaDocumentoDoc.objects.get(revisor=usuario, equipo=equipo, tipo='proyecto')
    numero_salas = sala_documento.salarevisardoc_set.count()
    salas_revisar = sala_documento.salarevisardoc_set.all()
    suma = 0
    for sala in salas_revisar:
        suma += sala.nota

    context = {
            'grupo':grupo,
            'sala_revisar': sala_revisar,
            'equipo': equipo,
            'form': form,
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
    # suma de nota max
    suma_max = 0
    for sala in salas_revisar:
        suma_max += sala.nota_max
    # calificacion
    for sala in salas_revisar:
        if sala.nota == 0:
            is_calificacion_todo = False
        else:
            is_calificacion_todo = True

    # cerrados, utilizare el is_calificado para este fin.
    vector_is_calificado = [v.is_calificado for v in salas_revisar]
    is_cerrado = all(vector_is_calificado)

    if grupo_revisor == 'tribunal':
        if actividadRealizadaEstudiante("visto bueno tribunal 1", sala_doc.equipo.datosestudiante_set.first()):
            texto_actividad = f"visto bueno {sala_doc.tipo} 2"
        else:
            texto_actividad = f"visto bueno {sala_doc.tipo} 1"
    else:
        texto_actividad = f"visto bueno {sala_doc.tipo} {sala_doc.revisor.groups.get()}"

    if request.method == 'POST':
        # if grupo_revisor == 'docente':
            # if sala_doc.tipo == 'perfil':
                # RegistroPerfil.objects.create(
                    # equipo = sala_doc.equipo,
                    # perfil = sala_doc.salarevisardoc_set.last().archivo_corregir,    
                # )
            # elif sala_doc.tipo == 'proyecto':
                # suma = 0
                # for sala in salas_revisar:
                    # suma += sala.nota
                # proyecto, created = ProyectoDeGrado.objects.get_or_create(equipo=equipo)
                # proyecto.nota_informes_trabajo = suma
                # proyecto.archivo = sala_doc.salarevisardoc_set.last().archivo_corregir    
                # proyecto.save()
        # agregarActividadEquipo('revisar proyecto', equipo)
        if grupo_revisor == 'docente' and sala_doc.tipo == "proyecto":
            suma = 0
            for sala in salas_revisar:
                suma += sala.nota
            proyecto, created = ProyectoDeGrado.objects.get_or_create(equipo=equipo)
            proyecto.nota_informes_trabajo = suma
            # proyecto.archivo = sala_doc.salarevisardoc_set.last().archivo_corregir    
            proyecto.save()
        sala_doc.visto_bueno = True
        sala_doc.save()
        agregarActividadEquipo(texto_actividad, sala_doc.equipo)
        return redirect('progreso_estudiante', pk=sala_doc.equipo.id)
    registro_perfil, created = RegistroPerfil.objects.get_or_create(
        equipo=sala_doc.equipo)
    registro_proyecto, created = ProyectoDeGrado.objects.get_or_create(
        equipo=sala_doc.equipo)
    context = {'sala_doc': sala_doc,
            'suma_max': suma_max,
            'is_calificacion_todo': is_calificacion_todo,
            'is_cerrado': is_cerrado,
            'registro_perfil': registro_perfil,
            'registro_proyecto': registro_proyecto,
            'grupo': grupo,
            }
    return render(request, 'revisar_documentos/dar_visto_bueno.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal'])
def registrarDocumento(request, id_sala_doc):
    sala_doc = get_object_or_404(SalaDocumentoDoc, id=id_sala_doc)
    grupo = request.user.groups.get().name
    equipo = sala_doc.equipo
    if sala_doc.tipo == "perfil":
        perfil = RegistroPerfil.objects.get(equipo=equipo)
        form = RegistroPerfilForm(instance=perfil)
        if request.method == 'POST':
            form = RegistroPerfilForm(request.POST, request.FILES, instance=perfil)
            if form.is_valid():
                form.save()
                if grupo == 'docente':
                    agregarActividadEquipo('registro perfil', equipo)
                return redirect('revisar_documentos:dar_visto_bueno', id_sala_doc=sala_doc.id)
    elif sala_doc.tipo == "proyecto":
        proyecto = ProyectoDeGrado.objects.get(equipo=equipo)
        form = RegistroProyectoDeGradoForm(instance=proyecto)
        if request.method == 'POST':
            form = RegistroProyectoDeGradoForm(request.POST, request.FILES, instance=proyecto)
            if form.is_valid():
                form.save()
                if grupo == 'docente':
                    agregarActividadEquipo('registro proyecto', equipo)
                return redirect('revisar_documentos:dar_visto_bueno', id_sala_doc=sala_doc.id)

    context = {
            'sala_doc': sala_doc,
            'form': form,
            'grupo': grupo,
            }
    return render(request, 'revisar_documentos/registrar_documento.html', context)

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
