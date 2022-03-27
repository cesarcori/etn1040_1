from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# modulos de activacion por email
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
UserModel = get_user_model()

from .decorators import unauthenticated_user, allowed_users, admin_only 
from .decorators import *
from .forms import *
from .models import *
from revisar.models import *
from actividades.models import *
from actividades.funciones import *
from .cartas import *
from .reportes import *
from .formularios import *
from .funciones import *

from random import randint
from datetime import timedelta,date 

from busquedas.funciones import searchByData, searchByDataExcel
from itertools import chain

# ********* activar o desactivar correo para pruebas *******
activar_estudiante = True
# **********************************************************
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
            password = form.cleaned_data.get('password1')
            nombre = form.cleaned_data.get('nombre')
            apellido = form.cleaned_data.get('apellido')
            carnet = form.cleaned_data.get('carnet')
            extension = form.cleaned_data.get('extension')
            registro_uni = form.cleaned_data.get('registro_uni')
            celular = form.cleaned_data.get('celular')
            mencion = form.cleaned_data.get('mencion')
            if User.objects.filter(username=usuario).exists():
                messages.info(request, 
            'No se envió la solicitud, un usuario ya usa este nombre de usuario')
            elif User.objects.filter(email=correo).exists():
                messages.info(request,
            'No se envió la solicitud, un usuario ya usa este correo electrónico')
            # elif SolicitudInvitado.objects.filter(correo=correo).exists():
                # messages.info(request, 
            # 'No se envió la solicitud, un solicitante usa este mismo correo electrónico')
            elif SolicitudInvitado.objects.filter(carnet=carnet).exists():
                messages.info(request, 
            'No se envió la solicitud, un solicitante usa este mismo número de carnet')
            elif SolicitudInvitado.objects.filter(registro_uni=registro_uni).exists():
                messages.info(request, 
            'No se envió la solicitud, un solicitante usa este mismo número de \
            registro universitario')
            # elif DatosEstudiante.objects.filter(correo=correo).exists():
                # messages.info(request, 
            # 'No se envió la solicitud, un estudiante usa este mismo correo electrónico')
            elif DatosEstudiante.objects.filter(carnet=carnet).exists():
                messages.info(request, 
            'No se envió la solicitud, un estudiante usa este mismo número de carnet')
            elif DatosEstudiante.objects.filter(registro_uni=registro_uni).exists():
                messages.info(request, 
            'No se envió la solicitud, un estudiante usa este mismo número de \
            registro universitario')
            else:
                # creacion del usuario
                User.objects.create_user(
                    username = usuario,
                    email = correo,
                    first_name = nombre,
                    last_name = apellido,
                    password = password,
                    )
                # creacion del grupo
                group = Group.objects.get(name='solicitud')
                user = User.objects.get(username=usuario)
                user.is_active = activar_estudiante
                user.groups.add(group)
                user.save()
                # creacion de datos del solicitante
                usuario_solicitud = User.objects.get(username=usuario)
                SolicitudInvitado.objects.create(
                    usuario = usuario_solicitud,
                    correo = correo,
                    nombre = nombre,
                    apellido = apellido,
                    carnet = carnet,
                    extension = extension,
                    registro_uni = registro_uni,
                    celular = celular,
                    mencion = mencion,
                    # password = password
                    )
                # email_activacion(request, user, correo)
                # messages.success(request, 'La solicitud se envió con exito!!! para activar tu cuenta debes de ingresar a tu correo electrónico y dar click en el enlace de activación: ')
                messages.success(request, 'La solicitud se envió con exito!!!: ')
    context = {'usuarios':usuarios, 'form':form}
    return render(request, 'proyecto/registro_estudiante.html', context)

@unauthenticated_user
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Gracias por confirmar tu registro, ahora puedes ingresar al sistema.')
    else:
        return HttpResponse('Activación de link invalido!')

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
    info = 'No se realizó ninguna acción'
    if request.method == 'POST':
        usuario_habi = request.POST.get('habilitar')
        usuario_elim = request.POST.get('eliminar') 
        if usuario_habi != None:
            info_usuario = SolicitudInvitado.objects.get(pk=usuario_habi)
            info = 'Se habilito al estudiante: ' + info_usuario.apellido + ' ' \
            + info_usuario.nombre
            # sorteo de grupo_docente
            docente_asignado = sorteoDocente(info_usuario)
            # creacion de datos del usuario
            # sin_tutor = User.objects.get(username='sin_tutor')
            DatosEstudiante.objects.create(
                    usuario = User.objects.get(username=info_usuario.usuario),
                    correo = info_usuario.correo,
                    nombre = info_usuario.nombre,
                    apellido = info_usuario.apellido,
                    carnet = info_usuario.carnet,
                    extension = info_usuario.extension,
                    registro_uni = info_usuario.registro_uni,
                    celular = info_usuario.celular,
                    mencion = info_usuario.mencion,
                    grupo_doc = docente_asignado,
                    # tutor = DatosTutor.objects.get(nombre='sin_tutor')
                    )
            estudiante = DatosEstudiante.objects.get(correo=info_usuario.correo)
            # creacion de salas docente-estudiante
            id_docente = str(DatosEstudiante.objects.last().grupo_doc.usuario_id)
            id_estudiante = str(DatosEstudiante.objects.last().usuario_id)
            nombre_sala = id_docente + id_estudiante
            Sala.objects.create(nombre_sala = nombre_sala)
            # cambiar de grupo
            group = Group.objects.get(name='estudiante')
            group2 = Group.objects.get(name='solicitud')
            user = User.objects.get(username=info_usuario.usuario)
            user.groups.add(group)
            user.groups.remove(group2)
            
            SolicitudInvitado.objects.get(pk=usuario_habi).delete()

        elif usuario_elim != None:
            info_usuario = SolicitudInvitado.objects.get(pk=usuario_elim)
            info = 'Se eliminó al estudiante: ' + info_usuario.apellido + ' ' \
            + info_usuario.nombre
            SolicitudInvitado.objects.get(pk=usuario_elim).usuario.delete()
        return redirect('home')
    solicitudes = SolicitudInvitado.objects.all()
    # aviso = 'Tiene: ' + str(solicitudes.count()) + ' solicitudes'
    aviso = f"Tiene: {solicitudes.count()} solicitudes"
    context = {'grupo': grupo, 'solicitudes':solicitudes,
            'form':form, 'info':info, 'aviso':aviso}
    return render(request, 'proyecto/home.html', context)

@login_required(login_url='login')
@admin_only
def eliminarUsuario(request, usuario_id):
    usuario = User.objects.get(pk=usuario_id)    
    eliminar = 'no'
    if request.method == 'POST':
        eliminar = request.POST['eliminar']
    if eliminar == 'si':
        usuario.delete()
        return redirect('home')
    context = {'usuario':usuario}
    return render(request, 'proyecto/eliminar_usuario.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente'])
def docente(request):
    grupo = 'docente'
    datos_est = request.user.datosdocente.datosestudiante_set.filter(
            Q(modalidad="individual") | Q(modalidad=None) | Q(is_modalidad_aprobada=False)
            )
    equipos_multiple = request.user.datosdocente.equipo_set.filter(cantidad__gt = 1)
    context = {'datos_est':datos_est,'grupo':grupo, 'equipos_multiple':equipos_multiple}
    return render(request, 'proyecto/docente.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor'])
def tutor(request):
    grupo = request.user.groups.get().name
    tutor = request.user.datostutor
    # datos_est = tutor.datosestudiante_set.filter(modalidad='individual').order_by('apellido')
    datos_est = [e.datosestudiante_set.get() for e in request.user.datostutor.equipo_set.filter(cantidad=1)]
    # equipos = Equipo.objects.filter(tutor=tutor).exclude(cantidad=1)
    equipos_multiple = request.user.datostutor.equipo_set.filter(cantidad__gt=1)
    datos_est = [n.datosestudiante_set.get() for n in Equipo.objects.filter(tutor=tutor, cantidad=1)]
    context = {'datos_est':datos_est,'grupo':grupo,'equipos_multiple':equipos_multiple}
    return render(request, 'proyecto/tutor.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tribunal'])
def tribunal(request):
    grupo = 'tribunal'
    # datos_est = request.user.datostribunal.datosestudiante_set.all().order_by('apellido')
    # datos_est = request.user.tribunal.equipo_set.filter(
            # Q(modalidad="individual") | Q(modalidad=None)
            # )
    tribunal = request.user.datostribunal
    datos_est = [e.datosestudiante_set.get() for e in tribunal.equipo_set.filter(cantidad=1)]
    equipos_multiple = tribunal.equipo_set.filter(cantidad__gt=1)
    context = {'datos_est':datos_est,'grupo':grupo,'equipos_multiple':equipos_multiple}
    return render(request, 'proyecto/tribunal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['director'])
def director(request):
    grupo = request.user.groups.get().name
    # datos_est = DatosEstudiante.objects.all().order_by('apellido')
    # context = {'datos_est':datos_est,'grupo':grupo}
    datos_est = DatosEstudiante.objects.filter(
            Q(modalidad="individual") | Q(modalidad=None)
            )
    equipos_multiple = Equipo.objects.filter(cantidad__gt=1)
    context = {'datos_est':datos_est,'grupo':grupo, 
            'equipos_multiple':equipos_multiple,}
    return render(request, 'proyecto/director.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['solicitud'])
def solicitud(request):
    grupo = 'solicitud'
    usuario = request.user.solicitudinvitado
    context = {'usuario':usuario,'grupo':grupo}
    return render(request, 'proyecto/solicitud.html', context)
    # return HttpResponse(f'Hola {usuario} su solicitud fue enviada con éxito')

@login_required(login_url='login')
@allowed_users(allowed_roles=['director'])
def asignarTribunal(request, pk):
    grupo = 'director'
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    equipo = Equipo.objects.get(id=pk)
    tribunal_estudiante = equipo.tribunales.all()
    tribunales_todos = DatosTribunal.objects.all()
    tribunales = tribunales_todos.difference(tribunal_estudiante).order_by('apellido')
    context = {'grupo':grupo, 'tribunales':tribunales,
            'equipo':equipo}
    return render(request, 'proyecto/asignar_tribunal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['director'])
def confirmarAsignarTribunal(request, pk_equi, id_trib):
    grupo = 'director'
    equipo = Equipo.objects.get(id=pk_equi)
    tribunal = DatosTribunal.objects.get(id=id_trib)
    if request.method == 'POST':
        confirmar_estudio = request.POST['confirmar']
        if confirmar_estudio == 'si':
            if equipo.tribunales.count() < 2:
                equipo.tribunales.add(tribunal)
                SalaDocumentoApp.objects.create(
                    revisor = tribunal.usuario,    
                    grupo_revisor = tribunal.usuario.groups.get(),
                    equipo = equipo,
                    tipo = 'tribunal',
                    )
                if equipo.tribunales.count() == 2:
                    agregarActividadEquipo("asignacion de tribunal", equipo)
            else:
                print('ya tiene dos tribunales')
            return redirect('asignar_tribunal', pk=pk_equi)
    context = {'grupo':grupo, 'tribunal':tribunal,
            'equipo':equipo}
    return render(request, 'proyecto/confirmar_asignar_tribunal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente'])
def firmas(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    if grupo == 'tutor':
        if Documentos.objects.filter(usuario=usuario).exists():
            documento = Documentos.objects.get(usuario=usuario)
            form = DocumentosForm(instance=documento)
            if request.method == 'POST':
                form = DocumentosForm(request.POST,instance=documento)
                if form.is_valid():
                    form.save()
                    return redirect('firmas')
        else:
            form = DocumentosForm()
            if request.method == 'POST':
                form = DocumentosForm(request.POST)
                if form.is_valid():
                    documentos = form.save(commit=False)
                    documentos.usuario = usuario
                    documentos.save()
                    return redirect('firmas')

    if grupo == 'docente':
        if Documentos.objects.filter(usuario=usuario).exists():
            documento = Documentos.objects.get(usuario=usuario)
            form = DocumentosDocenteForm(instance=documento)
            if request.method == 'POST':
                form = DocumentosDocenteForm(request.POST,instance=documento)
                if form.is_valid():
                    form.save()
                    return redirect('firmas')
        else:
            form = DocumentosDocenteForm()
            if request.method == 'POST':
                form = DocumentosDocenteForm(request.POST)
                if form.is_valid():
                    documentos = form.save(commit=False)
                    documentos.usuario = usuario
                    documentos.save()
                    return redirect('firmas')
    context = {'grupo': grupo,'form':form,'usuario':usuario}
    return render(request, 'proyecto/firmas.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente'])
# @permitir_paso6()
def cargarFirma(request):
    grupo = request.user.groups.get().name
    if grupo == 'tutor':
        tutor = request.user.datostutor
        form = FirmaTutorForm(instance=tutor)
        if request.method == 'POST':
            form = FirmaTutorForm(request.POST, request.FILES,instance=tutor)
            if form.is_valid():
                form.save()
                return redirect('firmas')
    if grupo == 'docente':
        docente = request.user.datosdocente
        form = FirmaDocenteForm(instance=docente)
        if request.method == 'POST':
            form = FirmaDocenteForm(request.POST, request.FILES,instance=docente)
            if form.is_valid():
                form.save()
                return redirect('firmas')
    context = {'grupo': grupo,'form':form,}
    return render(request, 'proyecto/cargar_firma.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente'])
# @permitir_paso6()
def documentosFirma(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    form = DocumentosForm()
    if request.method == 'POST':
        form = DocumentosForm(request.POST)
        if form.is_valid():
            documentos = form.save(commit=False)
            documentos.usuario = usuario
            # comunicado.save()
            return redirect('firmas')
    context = {'grupo': grupo,'form':form,}
    return render(request, 'proyecto/cargar_firma.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor'])
def solicitudTutoria(request, pk):
    grupo = request.user.groups.get().name
    tutor = request.user.datostutor
    equipo = get_object_or_404(Equipo, id=pk)
    # confirmar que el equipo pertenece al tutor
    if not tutor == equipo.tutor:
        return HttpResponse('error')
    docente = equipo.docente
    integrantes = equipo.datosestudiante_set.all()
    aceptar = 'no'
    rechazar = 'no'
    if request.method == 'POST':
        aceptar = request.POST.get('confirmar')
        rechazar = request.POST.get('rechazar') 
    if aceptar == 'si':
        equipo.tutor_acepto = True
        equipo.save()
        for estudiante in integrantes:
            actividad = Actividad.objects.get(nombre="tutor acepto")
            estudiante.actividad.add(actividad)
            estudiante.save()
        # crear sala de documento perfil tutor
        SalaDocumentoApp.objects.create(
            revisor = tutor.usuario,    
            grupo_revisor = tutor.usuario.groups.get(),
            equipo = equipo,
            tipo = 'perfil',
            )
        # creacion sala documento perfil docente
        SalaDocumentoApp.objects.create(
            revisor = docente.usuario,    
            grupo_revisor = docente.usuario.groups.get(),
            equipo = equipo,
            tipo = 'perfil',
            )
        return redirect('tutor')
    if rechazar == 'si':
        # estudiante.tutor = None
        # estudiante.save()
        return redirect('tutor')
    context = {'grupo':grupo,'equipo':equipo}
    return render(request, 'proyecto/solicitud_tutoria.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def estudiante(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    pasos_realizados = len(pasosRealizados(estudiante))
    solicitud_invitado = estudiante.invitado.filter(estado=None)
    context_aux = {}
    if estudiante.actividad.filter(nombre='registro cronograma').exists():
        context_aux = informarCronograma(estudiante.equipo.id)
        if not isinstance(context_aux, dict):
            context_aux = {}
            mensaje = infoCronograma(estudiante.id)
            return HttpResponse(mensaje)
    if estudiante.grupo_doc == None:
        sorteo = 'no'
        if request.method == 'POST':
            sorteo = request.POST['sorteo']
        if sorteo == 'si':
            # sorteo docente
            docente_asignado = sorteoDocente(estudiante)
            # mencion = estudiante.mencion
            # doc_mencion = DatosDocente.objects.filter(mencion=mencion)
            # cantidad_est1 = doc_mencion[0].datosestudiante_set.count()
            # cantidad_est2 = doc_mencion[1].datosestudiante_set.count()
            # if cantidad_est1 == cantidad_est2:
                # sorteo = randint(0,1)
                # docente_asignado = doc_mencion[sorteo]
            # elif cantidad_est1 < cantidad_est2:
                # docente_asignado = doc_mencion[0]
            # else:
                # docente_asignado = doc_mencion[1]
            # docente = doc_mencion[0]                   
            # guardar docente
            estudiante.grupo_doc = docente_asignado
            estudiante.save()
            # creacion de salas docente-estudiante
            id_docente = estudiante.grupo_doc.usuario_id.__str__()
            id_estudiante = estudiante.usuario_id.__str__()
            nombre_sala = id_docente + id_estudiante
            Sala.objects.create(nombre_sala = nombre_sala)
            return redirect('estudiante')
        return render(request, 'proyecto/sorteo_docente.html')
    else:
        progreso = progress(estudiante)
        context = {'grupo': grupo,'progreso':progreso, 'estudiante':estudiante,
                'solicitud_invitado':solicitud_invitado,'pasos_realizados':pasos_realizados}
        context = {**context, **context_aux}
        return render(request, 'proyecto/estudiante.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','estudiante','tribunal','director','administrador'])
def perfilUsuarios(request):
    grupo = request.user.groups.get().name
    context = {'grupo': grupo}
    return render(request, 'proyecto/perfil.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','estudiante','tribunal','director','administrador'])
def editarPerfil(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    if grupo == 'tutor':
        tutor = usuario.datostutor
        form = DatosTutorForm(instance=tutor)
        if request.method == "POST":
            form = DatosTutorForm(request.POST, request.FILES, instance=tutor)
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            if form.is_valid():
                form.save()
                usuario.first_name = nombre
                usuario.last_name = apellido
                usuario.save()
                return redirect('perfil')
    if grupo == 'docente':
        docente = usuario.datosdocente
        form = DatosDocenteForm(instance=docente)
        if request.method == "POST":
            form = DatosDocenteForm(request.POST, request.FILES, instance=docente)
            if form.is_valid():
                form.save()
                # nombre = request.POST.get('nombre')
                # apellido = request.POST.get('apellido')
                # usuario.first_name = nombre
                # usuario.last_name = apellido
                usuario.save()
                return redirect('perfil')
    if grupo == 'estudiante':
        estudiante = usuario.datosestudiante
        form = DatosEstudianteForm(instance=estudiante)
        if request.method == "POST":
            form = DatosEstudianteForm(request.POST, request.FILES, instance=estudiante)
            if form.is_valid():
                form.save()
                # nombre = request.POST.get('nombre')
                # apellido = request.POST.get('apellido')
                # usuario.first_name = nombre
                # usuario.last_name = apellido
                # usuario.save()
                return redirect('perfil')
    if grupo == 'administrador':
        administrador = usuario.datosadministrador
        form = DatosAdministradorForm(instance=administrador)
        if request.method == "POST":
            form = DatosAdministradorForm(request.POST, request.FILES, instance=administrador)
            if form.is_valid():
                form.save()
                nombre = request.POST.get('nombre')
                apellido = request.POST.get('apellido')
                correo = request.POST.get('correo')
                usuario.first_name = nombre
                usuario.last_name = apellido
                usuario.email = correo
                usuario.save()
                return redirect('perfil')
    if grupo == 'director':
        director = usuario.datosdirector
        form = DatosDirectorForm(instance=director)
        if request.method == "POST":
            form = DatosDirectorForm(request.POST, request.FILES, instance=director)
            if form.is_valid():
                nombre = request.POST.get('nombre')
                apellido = request.POST.get('apellido')
                correo = request.POST.get('correo')
                usuario.first_name = nombre
                usuario.last_name = apellido
                usuario.email = correo
                usuario.save()
                form.save()
                return redirect('perfil')
    if grupo == 'tribunal':
        tribunal = usuario.datostribunal
        form = DatosTribunalForm(instance=tribunal)
        if request.method == "POST":
            form = DatosTribunalForm(request.POST, request.FILES, instance=tribunal)
            if form.is_valid():
                form.save()
                nombre = request.POST.get('nombre')
                apellido = request.POST.get('apellido')
                usuario.first_name = nombre
                usuario.last_name = apellido
                usuario.save()
                return redirect('perfil')
    context = {'grupo': grupo,'form':form}
    return render(request, 'proyecto/editar_perfil.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','estudiante','tribunal','director','administrador'])
def editarPassword(request):
    grupo = request.user.groups.get().name
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'Contraseña actualizada!')
            return redirect('perfil')
        # else:
            # messages.error(request, 'Corrige el error de abajo.')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form,'grupo':grupo}
    return render(request, 'proyecto/editar_password.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','estudiante','tribunal','director','administrador'])
@admin_only
def resetearPassword(request, id_user):
    grupo = request.user.groups.get().name
    usuario = User.objects.get(id=id_user)
    if request.method == 'POST':
        confirmar = request.POST['confirmar']
        if confirmar == 'si':
            usuario.set_password(usuario.__str__())
            usuario.save()
            return redirect('home')
    context = {'usuario':usuario}
    return render(request, 'proyecto/resetear_password.html', context)

# Comunicados, docentes, tutores, y vista estudiantes
@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','estudiante'])
def misComunicados(request):
    grupo = str(request.user.groups.get())
    docente = User.objects.get(id=request.user.id)
    comunicados = docente.comunicado_set.all().order_by('-fecha_creacion')
    context = {'grupo': grupo, 'comunicados':comunicados}
    return render(request, 'proyecto/mis_comunicados.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','estudiante'])
def eliminarComunicado(request, id_comunicado):
    comunicado = get_object_or_404(Comunicado, id=id_comunicado)
    id_usuario = comunicado.autor.id
    if request.method == 'POST':
        comunicado.delete()
        return redirect('mis_comunicados')
    context = {'comunicado':comunicado}
    return render(request, 'proyecto/eliminar_comunicado.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','estudiante'])
def crearComunicado(request):
    grupo = request.user.groups.all()[0].name # es lo mismo que arriba
    if request.method == "POST":
        form = ComunicadoForm(request.POST)
        if form.is_valid():
            comunicado = form.save(commit=False)
            comunicado.autor= request.user
            comunicado.save()
            return redirect('mis_comunicados')
    else:
        form = ComunicadoForm()
    context = {'grupo': grupo, 'form':form}
    return render(request, 'proyecto/crear_comunicado.html', context)

# Esta sera la bandeja de entrada
@login_required(login_url='login')
def mensajePersonal(request, pk_doc_tut_est):
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def comunicadosDocEst(request):
    grupo = str(request.user.groups.get())
    id_docente = request.user.datosestudiante.grupo_doc.usuario_id
    docente = User.objects.get(id=id_docente)
    comunicados = docente.comunicado_set.all().order_by('-fecha_creacion')
    valor = 'docente'
    context = {'grupo': grupo, 'comunicados':comunicados, 'valor':valor}
    return render(request, 'proyecto/comunicado_estudiantes.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def comunicadosTutEst(request):
    grupo = request.user.groups.get().name
    # id_tutor= request.user.datosestudiante.tutor.usuario_id
    # tutor = User.objects.get(id=id_tutor)
    if request.user.datosestudiante.equipo.tutor == None:
        tutor = None
    else:
        tutor = request.user.datosestudiante.equipo.tutor.usuario
    if tutor:
        if Comunicado.objects.filter(autor=tutor).exists():
            comunicados = tutor.comunicado_set.all().order_by('-fecha_creacion')
        else:
            comunicados = None
    else:
        comunicados = None
    valor = 'tutor'
    context = {'grupo': grupo, 'comunicados':comunicados, 'valor':valor}
    return render(request, 'proyecto/comunicado_estudiantes.html', context)

# Compartir, mensajeria entre estudiantes y docentes y tutores
@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','estudiante'])
def compartirPersonal(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/compartir_personal.html', context)

# enlaces solicitantes, estudiantes, docentes y tutores
@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','administrador'])
def enlaceSolicitante(request, pk_sol):
    grupo = str(request.user.groups.get())
    estudiante = SolicitudInvitado.objects.get(id=pk_sol)
    context = {'grupo': grupo,'estudiante':estudiante}
    return render(request, 'proyecto/enlace_solicitante.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','administrador','director','tribunal'])
def enlaceEstudiante(request, pk_est):
    grupo = str(request.user.groups.get())
    estudiante = DatosEstudiante.objects.get(id=pk_est)
    if grupo=='administrador' or grupo=='director' or grupo=='tribunal':
        context = {'grupo': grupo,'estudiante':estudiante,}
        return render(request, 'proyecto/enlace_estudiante.html', context)
    elif grupo == 'docente':
        # evita que se un docente consulte otros estudiantes
        existe_est = request.user.datosdocente.datosestudiante_set.filter(id=pk_est).exists()
        if existe_est:
            context = {'grupo': grupo,'estudiante':estudiante,}
            return render(request, 'proyecto/enlace_estudiante.html', context)
        else:
            return HttpResponse('error')
    else:           
        tutor = request.user.datostutor
        if tutor.equipo_set.filter(tutor=tutor).exists():
            context = {'grupo': grupo,'estudiante':estudiante,}
            return render(request, 'proyecto/enlace_estudiante.html', context)
        else:
            return HttpResponse('error')

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','director'])
def enlaceEstudianteTitulado(request, id_est_tit):
    grupo = request.user.groups.get().name
    estudiante = DatosEstudianteTitulado.objects.get(id=id_est_tit)
    if grupo=='administrador' or grupo=='director':
        context = {'grupo': grupo,'estudiante':estudiante,}
        return render(request, 'proyecto/enlace_estudiante_titulado.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['estudiante','administrador','docente','tutor','director'])
# def imprimirReporteEstudiante(request, id_est):
    # buffer = io.BytesIO()
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    # usuario_solicitante = request.user
    # docReporteEstudiante(buffer, estudiante, usuario_solicitante)
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename='carta_aceptacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','administrador','director','tribunal'])
def progresoEstudiante(request, pk):
    grupo = request.user.groups.get().name
    equipo = Equipo.objects.get(id=pk)
    estudiante = equipo.datosestudiante_set.first()
    # estudiante = get_object_or_404(DatosEstudiante, id=pk)
    # equipo = estudiante.equipo
    progreso = progress(estudiante)
    # if equipo == None:
        # tribunales = None
    # else: 
        # tribunales = equipo.tribunales.all()
    tribunales = equipo.tribunales.all()
    is_nota_tribunal = False
    if ProyectoDeGrado.objects.filter(equipo=equipo).exists():
        proyecto = ProyectoDeGrado.objects.get(equipo=equipo)
        calificacion = proyecto.calificacion
    else:
        proyecto = None
        calificacion = None
    # cronograma informacion
    if equipo:
        context_aux = informarCronograma(equipo.id)
        if not isinstance(context_aux, dict):
            context_aux = {}
            mensaje = infoCronograma(estudiante.id)
            return HttpResponse(mensaje)
    else:
        context_aux={}
    if grupo == 'docente':
        # evita que se un docente consulte otros estudiantes
        # existe_est = request.user.datosdocente.datosestudiante_set.filter(id=pk).exists()
        existe_est = request.user.datosdocente.equipo_set.filter(id=pk).exists()
        if not existe_est:
            return HttpResponse('error')
    elif grupo== 'tutor':
        # existe_est = request.user.datostutor.datosestudiante_set.filter(id=pk).exists()
        # if not existe_est:
            # return HttpResponse('error')
        existe_est = request.user.datostutor.equipo_set.filter(id=pk).exists()
        if not existe_est:
            return HttpResponse('error')
    elif grupo== 'tribunal':
        tribunal = request.user.datostribunal
        existe_est = tribunal.equipo_set.filter(id=pk).exists()
        if not existe_est:
            # para que salga notificacion proyecto
            return HttpResponse('error')
        is_nota_tribunal = NotaTribunal.objects.filter(equipo=equipo, tribunal=tribunal)
    elif grupo== 'director':
        # existe_est = DatosEstudiante.objects.filter(id=pk).exists()
        existe_est = Equipo.objects.filter(id=pk).exists()
        if not existe_est:
            return HttpResponse('error')
    revisor = request.user
    usuario = request.user
    # documento = 'perfil'
    # sala_doc = SalaDocumentoApp.objects.get(revisor=revisor, 
        # grupo_revisor=revisor.groups.get(), estudiante=estudiante, tipo=documento)
    salas_doc_est = SalaDocumentoApp.objects.filter(equipo=equipo).exclude(revisor=revisor).order_by('-fecha_creacion')
    sala_doc = SalaDocumentoApp.objects.filter(revisor=revisor, 
        grupo_revisor=revisor.groups.get(), equipo=equipo).last()
    salas_revisar = SalaRevisarApp.objects.filter(sala_documento=sala_doc).order_by('-fecha_creacion')
    salas_doc = SalaDocumentoApp.objects.filter(equipo=equipo, tipo='tribunal')
    dicc_salas = {}
    for sala in salas_revisar:
        mensajes = MensajeRevisarApp.objects.filter(sala=sala).exclude(usuario=usuario)
        no_visto = 0
        for mensaje in mensajes:
            if not mensaje.visto:
                no_visto += 1
        dicc_salas[sala] = no_visto
    todo_salas_doc = SalaDocumentoApp.objects.filter(equipo=equipo)
    notas_tribunales = NotaTribunal.objects.filter(equipo=equipo)
    context = {'grupo': grupo,
            'estudiante':estudiante,
            'equipo': equipo,
            'progreso':progreso,
            'proyecto': proyecto,
            'calificacion': calificacion,
            'sala_doc':sala_doc,
            'dicc_salas':dicc_salas,
            'salas_doc_est':salas_doc_est,
            'salas_doc':salas_doc,
            'todo_salas_doc':todo_salas_doc,
            'is_nota_tribunal':is_nota_tribunal,
            'notas_tribunales':notas_tribunales,
            }
    context = {**context_aux, **context}
    return render(request, 'proyecto/progreso_estudiante.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['docente','tutor','administrador','director','tribunal'])
# def progresoEstudianteBackup(request, pk_est):
    # grupo = str(request.user.groups.get())
    # estudiante = DatosEstudiante.objects.get(id=pk_est)
    # progreso = Progreso.objects.get(usuario=estudiante).nivel
    # tribunales = estudiante.tribunales.all()
    # dicc_vb_tribunal = {}
    # for tribunal in tribunales:
        # salas = SalaRevisarTribunal.objects.filter(estudiante_rev=estudiante, tribunal_rev=tribunal) 
        # vb_tribunal = False
        # for sala in salas:
            # if sala.visto_bueno:
                # vb_tribunal = sala.visto_bueno
                # break
        # dicc_vb_tribunal[tribunal] = vb_tribunal
    # if ProyectoDeGrado.objects.filter(usuario=estudiante).exists():
        # proyecto = ProyectoDeGrado.objects.get(usuario=estudiante)
        # calificacion = proyecto.calificacion
    # else:
        # proyecto = None
        # calificacion = None
    # # cronograma informacion
    # context_aux = infoCronograma(estudiante.id)
    # if not isinstance(context_aux, dict):
        # context_aux = {}
        # mensaje = infoCronograma(estudiante.id)
        # return HttpResponse(mensaje)
    # if grupo == 'docente':
        # # evita que se un docente consulte otros estudiantes
        # existe_est = request.user.datosdocente.datosestudiante_set.filter(id=pk_est).exists()
        # if existe_est:
            # info_estu = SalaRevisar.objects.filter(estudiante_rev=estudiante)
            # salas = SalaRevisar.objects.filter(estudiante_rev=estudiante) 
            # info_estu_proy = SalaRevisarProyecto.objects.filter(estudiante_rev=estudiante)
            # salas_proy = SalaRevisarProyecto.objects.filter(estudiante_rev=estudiante) 
            # # para que salga notificacion perfil
            # dicc_salas = {}
            # for sala in salas:
                # mensajes_doc = MensajeDocenteRevisar.objects.filter(sala=sala)
                # no_visto= 0
                # for mensaje_doc in mensajes_doc:
                    # if not mensaje_doc.visto_docente:
                        # no_visto += 1
                # dicc_salas[sala] = no_visto
            # # para que salga notificacion proyecto
            # dicc_salas_proy = {}
            # for sala in salas_proy:
                # mensajes_doc = MensajeDocenteRevisarProyecto.objects.filter(sala=sala)
                # no_visto= 0
                # for mensaje_doc in mensajes_doc:
                    # if not mensaje_doc.visto_docente:
                        # no_visto += 1
                # dicc_salas_proy[sala] = no_visto
            # revisor = request.user
            # documento = 'perfil'
            # usuario = request.user
            # sala_doc = SalaDocumentoApp.objects.get(revisor=revisor, 
                # grupo_revisor=revisor.groups.get(), estudiante=estudiante, tipo=documento)
            # salas_revisar = SalaRevisarApp.objects.filter(sala_documento=sala_doc).order_by('-fecha_creacion')
            # dicc_salas = {}
            # for sala in salas_revisar:
                # mensajes = MensajeRevisarApp.objects.filter(sala=sala).exclude(usuario=usuario)
                # no_visto = 0
                # for mensaje in mensajes:
                    # if not mensaje.visto:
                        # no_visto += 1
                # dicc_salas[sala] = no_visto
            # context = {'grupo': grupo,'estudiante':estudiante,
                    # 'progreso':progreso,
                    # 'info_estu':info_estu,
                    # 'salas':salas,
                    # 'dicc_salas':dicc_salas,
                    # 'dicc_salas_proy':dicc_salas_proy,
                    # 'info_estu_proy':info_estu_proy,
                    # 'salas_proy':salas_proy,
                    # 'proyecto': proyecto,
                    # 'dicc_vb_tribunal':dicc_vb_tribunal,
                    # 'calificacion': calificacion,
                    # 'sala_doc':sala_doc,
                    # 'dicc_salas':dicc_salas,
                    # }
            # context = {**context_aux, **context}
            # return render(request, 'proyecto/progreso_estudiante.html', context)
        # else:
            # return redirect('error_pagina')
    # elif grupo== 'tutor':
        # existe_est = request.user.datostutor.datosestudiante_set.filter(id=pk_est).exists()
        # if existe_est:
            # info_estu = SalaRevisar.objects.filter(estudiante_rev=estudiante)
            # salas = SalaRevisar.objects.filter(estudiante_rev=estudiante) 
            # info_estu_proy = SalaRevisarProyecto.objects.filter(estudiante_rev=estudiante)
            # salas_proy = SalaRevisarProyecto.objects.filter(estudiante_rev=estudiante) 
            # # para que salga notificacion
            # dicc_salas = {}
            # for sala in salas:
                # mensajes_tut= MensajeTutorRevisar.objects.filter(sala=sala)
                # no_visto= 0
                # for mensaje_tut in mensajes_tut:
                    # if not mensaje_tut.visto_tutor:
                        # no_visto += 1
                # dicc_salas[sala] = no_visto
            # # para que salga notificacion proyecto
            # dicc_salas_proy = {}
            # for sala in salas_proy:
                # mensajes_tut= MensajeTutorRevisarProyecto.objects.filter(sala=sala)
                # no_visto= 0
                # for mensaje_tut in mensajes_tut:
                    # if not mensaje_tut.visto_tutor:
                        # no_visto += 1
                # dicc_salas_proy[sala] = no_visto
            # revisor = request.user
            # documento = 'perfil'
            # usuario = request.user
            # sala_doc = SalaDocumentoApp.objects.get(revisor=revisor, 
                # grupo_revisor=revisor.groups.get(), estudiante=estudiante, tipo=documento)
            # salas_revisar = SalaRevisarApp.objects.filter(sala_documento=sala_doc).order_by('-fecha_creacion')
            # dicc_salas = {}
            # for sala in salas_revisar:
                # mensajes = MensajeRevisarApp.objects.filter(sala=sala).exclude(usuario=usuario)
                # no_visto = 0
                # for mensaje in mensajes:
                    # if not mensaje.visto:
                        # no_visto += 1
                # dicc_salas[sala] = no_visto
            # # context = {
                    # # 'sala_doc':sala_doc,
                    # # 'dicc_salas':dicc_salas,
                    # # 'grupo':grupo.name,
                    # # }
            # context = {'grupo': grupo,'estudiante':estudiante,
                    # 'progreso':progreso,
                    # 'info_estu':info_estu,
                    # 'salas':salas,
                    # 'dicc_salas':dicc_salas,
                    # 'dicc_salas_proy':dicc_salas_proy,
                    # 'info_estu_proy':info_estu_proy,
                    # 'salas_proy':salas_proy,
                    # 'proyecto': proyecto,
                    # 'dicc_vb_tribunal':dicc_vb_tribunal,
                    # 'calificacion': calificacion,
                    # 'sala_doc':sala_doc,
                    # 'dicc_salas':dicc_salas,
                    # }
            # context = {**context_aux, **context}
            # return render(request, 'proyecto/progreso_estudiante.html', context)
        # else:
            # return redirect('error_pagina')
    # elif grupo== 'tribunal':
        # existe_est = request.user.datostribunal.datosestudiante_set.filter(id=pk_est).exists()
        # tribunal = request.user.datostribunal
        # if existe_est:
            # info_estu = SalaRevisarTribunal.objects.filter(estudiante_rev=estudiante)
            # salas = SalaRevisarTribunal.objects.filter(estudiante_rev=estudiante, tribunal_rev=tribunal) 
            # vb_tribunal = False
            # for sala in salas:
                # if sala.visto_bueno:
                    # vb_tribunal = sala.visto_bueno
                    # break
            # # para que salga notificacion
            # dicc_salas = {}
            # for sala in salas:
                # mensajes_trib = MensajeTribunalRevisar.objects.filter(sala=sala)
                # no_visto = 0
                # for mensaje_trib in mensajes_trib:
                    # if not mensaje_trib.visto_tribunal:
                        # no_visto += 1
                # dicc_salas[sala] = no_visto
            # # para que salga notificacion proyecto
            # context = {'grupo': grupo,'estudiante':estudiante,
                    # 'progreso':progreso,
                    # 'info_estu':info_estu,
                    # 'salas':salas,
                    # 'dicc_salas':dicc_salas,
                    # 'proyecto': proyecto,
                    # 'vb_tribunal':vb_tribunal,
                    # 'calificacion': calificacion,
                    # }
            # context = {**context_aux, **context}
            # return render(request, 'proyecto/progreso_estudiante.html', context)
        # else:
            # return redirect('error_pagina')
    # elif grupo== 'director':
        # existe_est = DatosEstudiante.objects.filter(id=pk_est).exists()
        # if existe_est:
            # context = {'grupo': grupo,'estudiante':estudiante,
                    # 'progreso':progreso,
                    # 'proyecto': proyecto,
                    # 'dicc_vb_tribunal':dicc_vb_tribunal,
                    # 'calificacion': calificacion,
                    # }
            # context = {**context_aux, **context}
            # return render(request, 'proyecto/progreso_estudiante.html', context)
        # else:
            # return redirect('error_pagina')

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['docente','tutor'])
# def vistoBuenoPerfil(request, id_est):
    # grupo = request.user.groups.get().name
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    # visto_bueno = 'no'
    # if request.method == 'POST':
        # visto_bueno = request.POST['visto_bueno']
    # if visto_bueno == 'si':
        # if grupo == 'docente':
            # estudiante.vb_perfil_docente = True
        # else:
            # estudiante.vb_perfil_tutor = True
        # estudiante.save()
        # return redirect('progreso_estudiante',pk_est=id_est)
    # context = {'grupo': grupo}
    # return render(request, 'proyecto/visto_bueno_perfil.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['docente','tutor'])
# def vistoBuenoProyecto(request, id_est):
    # grupo = request.user.groups.get().name
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    # visto_bueno = 'no'
    # if request.method == 'POST':
        # visto_bueno = request.POST['visto_bueno']
    # if visto_bueno == 'si':
        # if grupo == 'docente':
            # estudiante.vb_proyecto_docente = True
        # else:
            # estudiante.vb_proyecto_tutor = True
        # estudiante.save()
        # return redirect('progreso_estudiante',pk_est=id_est)
    # context = {'grupo': grupo}
    # return render(request, 'proyecto/visto_bueno_proyecto.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['tribunal'])
# def vistoBuenoTribunal(request, id_est):
    # grupo = request.user.groups.get().name
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    # tribunal = request.user.datostribunal
    # visto_bueno = 'no'
    # if request.method == 'POST':
        # visto_bueno = request.POST['visto_bueno']
    # if visto_bueno == 'si':
        # sala = SalaRevisarTribunal.objects.filter(estudiante_rev=estudiante, tribunal_rev=tribunal).last() 
        # vb_tribunal = sala.visto_bueno = True
        # sala.save()
        # return redirect('progreso_estudiante',pk_est=id_est)
    # context = {'grupo': grupo}
    # return render(request, 'proyecto/visto_bueno_tribunal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','administrador','director','tribunal'])
def enlaceDocente(request, pk_doc):
    grupo = request.user.groups.get().name
    # docente = DatosDocente.objects.get(id=pk_doc)
    docente = get_object_or_404(DatosDocente, id=pk_doc)
    if grupo == 'administrador':
        estudiantes = docente.datosestudiante_set.all()
        context = {'grupo': grupo, 'estudiantes':estudiantes, 'docente':docente}
        return render(request, 'proyecto/enlace_docente.html', context)
    elif grupo == 'director':
        estudiantes = docente.datosestudiante_set.all()
        context = {'grupo': grupo, 'estudiantes':estudiantes, 'docente':docente}
        return render(request, 'proyecto/enlace_docente.html', context)
    elif grupo == 'estudiante':
        # user_request = request.user.datosestudiante.grupo_doc.id
        # obj_pk = docente.id
        # if user_request == obj_pk:
            # estudiantes = {}
            # context = {'grupo': grupo, 'estudiantes':estudiantes, 'docente':docente}
            # return render(request, 'proyecto/enlace_docente.html', context)
        # else:
            # # return redirect('error_pagina')
            # raise PermissionDenied
        docente = request.user.datosestudiante.grupo_doc
        estudiantes = {}
        context = {'grupo': grupo, 'estudiantes':estudiantes, 'docente':docente}
        return render(request, 'proyecto/enlace_docente.html', context)
    elif grupo == 'tutor':
        objeto_tutor_estu = request.user.datostutor.datosestudiante_set
        existe_doc = objeto_tutor_estu.filter(grupo_doc_id=pk_doc).exists()
        if existe_doc:
            estudiantes = {}
            context = {'grupo': grupo, 'estudiantes':estudiantes, 'docente':docente}
            return render(request, 'proyecto/enlace_docente.html', context)
        else:
            return redirect('error_pagina')
    elif grupo == 'tribunal':
        objeto_trib_est= request.user.datostribunal.datosestudiante_set
        existe_doc = objeto_trib_est.filter(grupo_doc_id=pk_doc).exists()
        if existe_doc:
            estudiantes = {}
            context = {'grupo': grupo, 'estudiantes':estudiantes, 'docente':docente}
            return render(request, 'proyecto/enlace_docente.html', context)
        else:
            return redirect('error_pagina')

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','administrador','estudiante','director'])
def enlaceTutor(request, pk_tutor):
    grupo = str(request.user.groups.get())
    tutor = DatosTutor.objects.get(id=pk_tutor)
    if grupo == 'docente':
        objeto_tutor_estu = request.user.datosdocente.datosestudiante_set
        existe_doc = objeto_tutor_estu.filter(tutor_id=pk_tutor).exists()
        if existe_doc:
            context = {'grupo': grupo, 'tutor':tutor}
            return render(request, 'proyecto/enlace_tutor.html', context)
        else:
            return HttpResponse('error')
    elif grupo == 'administrador':
        context = {'grupo': grupo, 'tutor':tutor}
        return render(request, 'proyecto/enlace_tutor.html', context)
    elif grupo == 'director':
        context = {'grupo': grupo, 'tutor':tutor}
        return render(request, 'proyecto/enlace_tutor.html', context)
    elif grupo == 'estudiante':
        id_tutor = request.user.datosestudiante.equipo.tutor.id
        if id_tutor == pk_tutor:
            context = {'grupo': grupo, 'tutor':tutor}
            return render(request, 'proyecto/enlace_tutor.html', context)
        else:
            return HttpResponse('error')

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','administrador','estudiante','director','tutor'])
def enlaceTribunal(request, pk_tribunal):
    grupo = str(request.user.groups.get())
    tribunal = DatosTribunal.objects.get(id=pk_tribunal)
    if grupo == 'docente':
        docente = request.user.datosdocente
        existe_doc = tribunal.equipo_set.filter(docente=docente).exists()
        if existe_doc:
            context = {'grupo': grupo, 'tribunal':tribunal}
            return render(request, 'proyecto/enlace_tribunal.html', context)
        else:
            return redirect('error_pagina')
    elif grupo == 'tutor':
        tutor = request.user.datostutor
        existe_doc = tribunal.equipo_set.filter(tutor=tutor).exists()
        if existe_doc:
            context = {'grupo': grupo, 'tribunal':tribunal}
            return render(request, 'proyecto/enlace_tribunal.html', context)
        else:
            return redirect('error_pagina')
    elif grupo == 'administrador':
        context = {'grupo': grupo, 'tribunal':tribunal}
        return render(request, 'proyecto/enlace_tribunal.html', context)
    elif grupo == 'director':
        context = {'grupo': grupo, 'tribunal':tribunal}
        return render(request, 'proyecto/enlace_tribunal.html', context)
    elif grupo == 'estudiante':
        trib = request.user.datosestudiante.equipo.tribunales.all()
        if pk_tribunal == trib[0].id or pk_tribunal == trib[1].id:
            context = {'grupo': grupo, 'tribunal':tribunal}
            return render(request, 'proyecto/enlace_tribunal.html', context)
        else:
            return redirect('error_pagina')

@login_required(login_url='login')
@admin_only
def registroEstudiante(request):
    grupo = request.user.groups.get().name
    context = {'grupo': grupo}
    return render(request, 'proyecto/registro_estudiante.html', context)

# Lista estudiantes, docentes, estudiantes, tutores
@login_required(login_url='login')
@admin_only
def listaEstudiantes(request):
    datos_est = DatosEstudiante.objects.all().order_by('apellido')
    context = {'datos_est':datos_est}
    return render(request, 'proyecto/lista_estudiante.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['director'])
def listaEstudianteTitulado(request):
    grupo = request.user.groups.get().name
    datos_est = DatosEstudianteTitulado.objects.all().order_by('fecha_conclusion')
    context = {'grupo':grupo,'datos_est':datos_est}
    return render(request, 'proyecto/lista_estudiante_titulado.html', context)

@login_required(login_url='login')
# @admin_only
@allowed_users(allowed_roles=['director','administrador',])
def listaDocentes(request):
    grupo = request.user.groups.get().name
    docentes = DatosDocente.objects.all().order_by('grupo')
    context = {'grupo':grupo,'docentes':docentes}
    return render(request, 'proyecto/lista_docente.html', context)

@login_required(login_url='login')
# @admin_only
@allowed_users(allowed_roles=['director','administrador',])
def listaTutores(request):
    grupo = request.user.groups.get().name
    tutores= DatosTutor.objects.all().order_by('apellido')
    context = {'grupo':grupo,'tutores':tutores}
    return render(request, 'proyecto/lista_tutores.html', context)

# Agregar docentes, tutores al sistema
@login_required(login_url='login')
@admin_only
def agregarDocente(request):
    form = FormDocente
    if request.method == 'POST':
        form = FormDocente(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            apellido = form.cleaned_data.get('apellido')
            grupo = form.cleaned_data.get('grupo')
            mencion = form.cleaned_data.get('mencion')
            # primer_apellido= apellido.split()[0].lower()
            # correo = primer_apellido+'_docente@gmail.com'
            # usuario = primer_apellido+'_docente'
            # password = primer_apellido+'_docente'

            correo = form.cleaned_data.get('correo')
            usuario = correo.split('@')[0] + "_docente"
            password = usuario

            est = DatosEstudiante.objects.filter(correo=correo).exists()
            sol = SolicitudInvitado.objects.filter(correo=correo).exists()
            di = DatosDirector.objects.filter(correo=correo).exists()
            adm = DatosAdministrador.objects.filter(correo=correo).exists()
            do = DatosDocente.objects.filter(correo=correo).exists()

            if est or sol or di or adm or do:
                messages.info(request,
            'No se agregó al Docente. Un docente, estudiante, director, administrador o solicitante; usa este mismo correo electrónico.')


            # if User.objects.filter(username=usuario).exists():
                # messages.info(request, 
            # 'No se agregó al docente, un docente usa este nombre de usuario')
            # elif User.objects.filter(email=correo).exists():
                # messages.info(request,
            # 'No se agregó al docente, un docente usa este mismo correo\
            # electrónico')
            elif DatosDocente.objects.filter(grupo=grupo).exists():
                messages.info(request, 
            'No se agregó al docente, otro docente ya se asigno a este grupo')

            else:                 
                # creacion del usuario
                User.objects.create_user(
                        username = usuario,
                        email = correo,
                        first_name = nombre,
                        last_name = apellido,
                        password = usuario,
                        )
                group = Group.objects.get(name='docente')
                user = User.objects.get(username=usuario)
                user.groups.add(group)
                user.is_active = True
                user.save()
                # creacion de datos
                DatosDocente.objects.create(
                        usuario = user,
                        correo = correo,
                        nombre = nombre,
                        apellido = apellido,
                        celular = 'sin llenar',
                        grupo = grupo,
                        mencion = mencion,
                        )
                # email_activacion(request, user, correo)
                messages.success(request, 'La solicitud se envió con exito!!!')
    context = {'form':form}
    return render(request, 'proyecto/agregar_docente.html', context)

@login_required(login_url='login')
@admin_only
def agregarTutor(request):
    form = TutorForm
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data.get('correo')
            usuario = correo.split('@')[0] + "_tutor"
            password = usuario

            est = DatosEstudiante.objects.filter(correo=correo).exists()
            sol = SolicitudInvitado.objects.filter(correo=correo).exists()
            di = DatosDirector.objects.filter(correo=correo).exists()
            adm = DatosAdministrador.objects.filter(correo=correo).exists()

            if est or sol or di or adm:
                messages.info(request,
            'No se agregó al tutor. Un estudiante, docente, administrador o solicitante; usa este mismo correo electrónico.')
            else:                 
                # creacion del usuario
                User.objects.create_user(
                        username = usuario,
                        email = correo,
                        first_name = 'sin llenar',
                        last_name = 'sin llenar',
                        password = password,
                        )
                group = Group.objects.get(name='tutor')
                user = User.objects.get(username=usuario)
                user.groups.add(group)
                user.is_active = True
                user.save()
                # creacion de datos
                DatosTutor.objects.create(
                        usuario = user,
                        correo = correo,
                        nombre = 'sin llenar',
                        apellido = 'sin llenar',
                        celular = 'sin llenar',
                        )
                # email_activacion(request, user, correo)
                messages.success(request, 'La solicitud se envió con éxito!!!')
    context = {'form':form}
    return render(request, 'proyecto/agregar_tutor.html', context)

@login_required(login_url='login')
@admin_only
def agregarTribunal(request):
    form = TribunalForm
    if request.method == 'POST':
        form = TribunalForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data.get('correo')
            usuario = correo.split('@')[0] + "_tribunal"
            password = usuario
            # if User.objects.filter(email=correo).exists():
                # messages.info(request,
            # 'No se agregó al tribunal, un usuario usa este mismo correo\
            # electrónico')

            est = DatosEstudiante.objects.filter(correo=correo).exists()
            sol = SolicitudInvitado.objects.filter(correo=correo).exists()
            di = DatosDirector.objects.filter(correo=correo).exists()
            adm = DatosAdministrador.objects.filter(correo=correo).exists()

            if est or sol or di or adm:
                messages.info(request,
            'No se agregó al Tribunal. Un estudiante, docente, administrador o solicitante; usa este mismo correo electrónico.')
            else:                 
                # creacion del usuario
                User.objects.create_user(
                        username = usuario,
                        email = correo,
                        first_name = 'sin llenar',
                        last_name = 'sin llenar',
                        password = usuario,
                        )
                group = Group.objects.get(name='tribunal')
                user = User.objects.get(username=usuario)
                user.groups.add(group)
                user.is_active = True
                user.save()
                # creacion de datos
                DatosTribunal.objects.create(
                        usuario = user,
                        correo = correo,
                        nombre = user.first_name,
                        apellido = user.last_name,
                        celular = 'sin llenar',
                        )
                # email_activacion(request, user, correo)
                messages.success(request, 'La solicitud se envió con éxito!!!')
    context = {'form':form}
    return render(request, 'proyecto/agregar_tribunal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def paso1(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante

    # vista material docente
    usuario_docente = estudiante.grupo_doc.usuario
    material_docente = MaterialDocente.objects.filter(propietario=usuario_docente)
    dicc_material = {}
    for material in material_docente:
        if material.vistamaterialdocente_set.filter(usuario=estudiante).exists():
            dicc_material[material] = True
        else:
            dicc_material[material] = False

    # vista reglamento
    reglamentos = Reglamento.objects.all()
    dicc_reglamento = {}
    for reglamento in reglamentos:
        if reglamento.vistareglamento_set.filter(usuario=estudiante).exists():
            dicc_reglamento[reglamento] = True
        else:
            dicc_reglamento[reglamento] = False
    
    # estudiar todos reglamentos
    leido = []
    for reglamento, estudiar in dicc_reglamento.items():
        leido.append(estudiar)
    estudio_reglamento_completado = all(leido)
    if all(leido):
        actividad = Actividad.objects.get(nombre='estudiar reglamentos')
        estudiante.actividad.add(actividad)

    # estudiar todos materiales del docente
    leido = []
    for material, estudiar in dicc_material.items():
        leido.append(estudiar)
    estudio_reglamento_completado = all(leido)
    if all(leido):
        actividad = Actividad.objects.get(nombre='material docente')
        estudiante.actividad.add(actividad)

    context = {'grupo': grupo, 
            'material_docente':material_docente,
            'estudiante':estudiante,
            'dicc_reglamento':dicc_reglamento,
            'dicc_material':dicc_material,
            }
    return render(request, 'proyecto/estudiante_paso1.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def confirmarReglamento(request,id_reg):
    grupo = request.user.groups.get().name
    reglamento = Reglamento.objects.get(id=id_reg)
    estudiante = request.user.datosestudiante
    if request.method == 'POST':
        confirmar_estudio = request.POST['confirmar']
        if confirmar_estudio == 'si':
            if not VistaReglamento.objects.filter(usuario = estudiante, reglamento_visto=reglamento).exists():
                VistaReglamento.objects.create(usuario=estudiante, reglamento_visto=reglamento)
            return redirect('paso1')
    context = {'grupo': grupo, 'reglamento':reglamento, }
    return render(request, 'proyecto/confirmar_reglamento.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def confirmarMaterialDocente(request,id_mat):
    grupo = request.user.groups.get().name
    material = MaterialDocente.objects.get(id=id_mat)
    estudiante = request.user.datosestudiante
    docente = estudiante.grupo_doc
    if request.method == 'POST':
        confirmar_estudio = request.POST['confirmar']
        if confirmar_estudio == 'si':
            if not VistaMaterialDocente.objects.filter(usuario=estudiante,
                    docente=docente, material_docente_visto=material).exists():
                VistaMaterialDocente.objects.create(usuario=estudiante, docente=docente, material_docente_visto=material)
            return redirect('paso1')
    context = {'grupo': grupo,'material': material}
    return render(request, 'proyecto/confirmar_material_docente.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
# @permitir_paso2()
@permitir_con(pasos=[1])
def paso2(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    progreso = progress(estudiante)
    busqueda_proyecto = estudiante.actividad.filter(nombre='busqueda proyecto').exists()
    query, buscado = None, ""
    if request.method == 'POST':
        buscado = request.POST['buscado']
        query_db = searchByData(buscado)
        query_excel = searchByDataExcel(buscado)
        query = list(chain(query_db, query_excel))
    context = {'grupo': grupo,'query':query,'buscado':buscado,'busqueda_proyecto':busqueda_proyecto}
    return render(request, 'proyecto/estudiante_paso2.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1])
def confirmarPaso2(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    if request.method == 'POST':
        actividad = Actividad.objects.get(nombre='busqueda proyecto')
        estudiante.actividad.add(actividad)
        estudiante.save()
        return redirect('paso2')
    context = {'grupo': grupo,}
    return render(request, 'proyecto/confirmar_paso.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2])
def paso3(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    # tutor = estudiante.equipo.tutor
    if estudiante.equipo: 
        tutor = estudiante.equipo.tutor
        integrantes = estudiante.equipo.datosestudiante_set.all()
    else: 
        tutor = None 
        integrantes = None
    elegir_modalidad = estudiante.actividad.filter(nombre="elegir modalidad").exists()
    rechazo = estudiante.rechazarsolicitud_set.last()
    # registro de tutor
    if request.method == 'POST':
        correo = request.POST['agregar_tutor']

        est = DatosEstudiante.objects.filter(correo=correo).exists()
        sol = SolicitudInvitado.objects.filter(correo=correo).exists()
        di = DatosDirector.objects.filter(correo=correo).exists()
        adm = DatosAdministrador.objects.filter(correo=correo).exists()

        if est or sol or di or adm:
            messages.info(request,
        'No se agregó al Tutor. Un estudiante, director, administrador o solicitante; usa este mismo correo electrónico.')
        else: 
            # si el tutor ya fue registrado
            if DatosTutor.objects.filter(correo=correo).exists():
                equipo = estudiante.equipo
                equipo.tutor = DatosTutor.objects.get(correo=correo)
                equipo.docente = estudiante.grupo_doc
                equipo.save()
                # creacion de salas tutor-estudiante
                for integrante in integrantes:
                    id_tutor = str(DatosTutor.objects.get(correo=correo).usuario_id)
                    id_estudiante = str(integrante.usuario.id)
                    nombre_sala = id_tutor + id_estudiante
                    Sala.objects.create(nombre_sala = nombre_sala)
                    actividad = Actividad.objects.get(nombre='solicitud tutoria')
                    integrante.actividad.add(actividad)
            else: 
                usuario = correo.split('@')[0] + '_tutor'
                # creacion de usuario tutor
                User.objects.create_user(
                        username = usuario,
                        email = correo,
                        first_name = 'sin llenar',
                        last_name = 'sin llenar',
                        password = usuario,
                        )
                # agregando a grupo tutor
                group = Group.objects.get(name='tutor')
                user = User.objects.get(email=correo)
                user.groups.add(group)
                user.is_active = True
                user.save()
                DatosTutor.objects.create(
                    usuario = user,
                    correo = correo,
                    nombre = user.first_name,
                    apellido= user.last_name,
                    celular= 'sin llenar',
                        )
                # relacionando equipo con tutor
                equipo = estudiante.equipo
                equipo.tutor = DatosTutor.objects.get(correo=correo)
                equipo.docente = estudiante.grupo_doc
                equipo.save()
                # creacion de salas tutor-estudiante
                for integrante in integrantes:
                    id_tutor = str(DatosTutor.objects.get(correo=correo).usuario_id)
                    id_estudiante = str(integrante.usuario.id)
                    nombre_sala = id_tutor + id_estudiante
                    Sala.objects.create(nombre_sala = nombre_sala)
                    actividad = Actividad.objects.get(nombre='solicitud tutoria')
                    integrante.actividad.add(actividad)
                # activacion por email
                # email_activacion(request, user, correo)
                messages.success(request, 'La solicitud se envió con éxito!!!')
        return redirect('paso3')
    mensaje = 'Ya se le asigno el tutor'
    imprimir = estudiante.actividad.filter(nombre='imprimir carta tutoria').exists()
    context = {'grupo': grupo, 'tutor':tutor, 'estudiante':estudiante,
            'elegir_modalidad':elegir_modalidad, 'rechazo':rechazo,'imprimir':imprimir}
    return render(request, 'proyecto/estudiante_paso3.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director','tribunal'])
def reporteTutorAcepto(request, id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    reporte_tutor_acepto(buffer, estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte_aceptacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2])
def confirmarPaso3(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    if not estudiante.actividad.filter(nombre='tutor acepto'):
        return HttpResponse('error')
    if request.method == 'POST':
        agregarActividadEquipo('imprimir carta tutoria', estudiante.equipo)
        return redirect('estudiante')
    context = {'grupo': grupo,}
    return render(request, 'proyecto/confirmar_paso.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3])
def paso4(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    tutor = estudiante.equipo.tutor
    docente = estudiante.grupo_doc
    registro_perfil_existe = RegistroPerfil.objects.filter(equipo=estudiante.equipo).exists()
    progreso = progress(estudiante)
    perfil = RegistroPerfil.objects.filter(equipo=estudiante.equipo)
    imprimir = actividadRealizadaEstudiante('imprimir formulario', estudiante)
    # nueva app revision
    sala_doc = SalaDocumentoApp.objects.get(equipo=estudiante.equipo, revisor=estudiante.equipo.tutor.usuario, tipo='perfil')
    if sala_doc.visto_bueno:
        sala_doc = SalaDocumentoApp.objects.get(equipo=estudiante.equipo, revisor=docente.usuario, tipo='perfil')
    context = {'grupo': grupo,'registro_perfil_existe': registro_perfil_existe,
            'progreso': progreso,'perfil':perfil,'estudiante':estudiante,
            'sala_doc': sala_doc,'imprimir':imprimir}
    return render(request, 'proyecto/estudiante_paso4.html', context)

@permitir_con(pasos=[1,2,3])
@login_required(login_url='login')
def carta_aceptacion_tutor(request):
    buffer = io.BytesIO()
    estudiante = request.user.datosestudiante
    carta_aceptacion(buffer, estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_aceptacion.pdf')

@permitir_con(pasos=[1,2,3])
@login_required(login_url='login')
def carta_solicitud_tutor(request):
    buffer = io.BytesIO()
    estudiante = request.user.datosestudiante
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    extension = 'L.P.'
    cargo = 'director'
    lugar = 'instituto de electrónica aplicada'
    institucion = 'facultad de ingeniería'
    info_estu = [
            estudiante.__str__(),
            estudiante.carnet,
            estudiante.extension,
            estudiante.celular,
            estudiante.correo,
            estudiante.grupo_doc.__str__(),
            estudiante.tutor.__str__(),
            cargo, lugar, institucion, 
            ]
    carta_solicitud(buffer,info_estu)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_solicitud.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3])
def registro_perfil(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    if request.method == "POST":
        form= RegistroPerfilForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.equipo = estudiante.equipo
            form.save()
            agregarActividadEquipo('registro perfil', estudiante.equipo)
            return redirect('paso4')
    else:
        form = RegistroPerfilForm()
    context = {'grupo': grupo, 'form':form,}
    return render(request, 'proyecto/registro_perfil.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3])
def ver_perfil_registrado(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    perfil = RegistroPerfil.objects.get(equipo=estudiante.equipo)
    context = {'grupo': grupo,'perfil':perfil}
    return render(request, 'proyecto/ver_perfil_registrado.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3])
def cronograma_actividad(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    cronograma = ActividadesCronograma.objects.filter(equipo=estudiante.equipo)
    existe_cronograma = RegistroCronograma.objects.filter(equipo=estudiante.equipo).exists()
    if existe_cronograma:
        registro_cronograma = RegistroCronograma.objects.get(equipo=estudiante.equipo)
    else: 
        registro_cronograma = ''
    if cronograma.exists():
        max_semana = range(1,1+max([n.semana_final for n in cronograma]))
        vector_final = []
        for c in cronograma:
            # print(cronograma[n-1])
            vector = []
            for n in max_semana:
                if n < c.semana_inicial or n > c.semana_final:
                    vector.append(' ')
                else:
                    vector.append('*')
            vector_final.append(vector)
        dicc_crono = {}
        for n in range(len(cronograma)):
            dicc_crono[cronograma[n]] = vector_final[n]
    else:
        max_semana = range(0)
        dicc_crono = {}
    if request.method == "POST":
        form= ActividadesCronogramaForm(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.equipo = estudiante.equipo
            file.save()
            return redirect('cronograma_actividad')
    else:
        form = ActividadesCronogramaForm()
        context = {'grupo': grupo,'form':form,'cronograma':cronograma, 
                'max_semana': max_semana,
                'dicc_crono':dicc_crono,
                'registro_cronograma': registro_cronograma,
                'existe_cronograma': existe_cronograma}
        return render(request, 'proyecto/cronograma_actividad.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','director','tribunal'])
def ver_cronograma(request, pk):
    grupo = request.user.groups.get().name
    if grupo == 'tutor':
        # estudiante = request.user.datostutor.datosestudiante_set.get(id=id_est)
        equipo = request.user.datostutor.equipo_set.get(id=pk)
    elif grupo == 'director':
        # estudiante = DatosEstudiante.objects.get(id=id_est)
        equipo = Equipo.objects.get(id=pk)
    elif grupo == 'docente':
        # estudiante = request.user.datosdocente.datosestudiante_set.get(id=id_est)
        equipo = request.user.datosdocente.equipo_set.get(id=pk)
    elif grupo == 'tribunal':
        # estudiante = request.user.datostribunal.datosestudiante_set.get(id=id_est)
        equipo = request.user.datostribunal.equipo_set.get(id=pk)
    cronograma = ActividadesCronograma.objects.filter(equipo=equipo)
    existe_cronograma = RegistroCronograma.objects.filter(equipo=equipo).exists()
    if cronograma.exists():
        max_semana = range(1,1+max([n.semana_final for n in cronograma]))
        vector_final = []
        for c in cronograma:
            # print(cronograma[n-1])
            vector = []
            for n in max_semana:
                if n < c.semana_inicial or n > c.semana_final:
                    vector.append(' ')
                else:
                    vector.append('*')
            vector_final.append(vector)
        dicc_crono = {}
        for n in range(len(cronograma)):
            dicc_crono[cronograma[n]] = vector_final[n]
    else:
        max_semana = range(0)
        dicc_crono = {}
    # fecha del registro
    registro_cronograma = RegistroCronograma.objects.get(equipo=equipo)
    context = {'grupo': grupo,'cronograma':cronograma, 
            'max_semana': max_semana,
            'equipo': equipo,
            'dicc_crono': dicc_crono,
            'registro_cronograma': registro_cronograma,
            'existe_cronograma': existe_cronograma}
    return render(request, 'proyecto/cronograma_actividad.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3])
def cronograma_registrar(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    form= RegistroCronogramaForm
    if request.method == "POST":
        form= RegistroCronogramaForm(request.POST)
        if form.is_valid():
            form.instance.equipo = estudiante.equipo
            form.save()
            agregarActividadEquipo('registro cronograma', estudiante.equipo)
            return redirect('paso4')
    context = {'grupo': grupo,'form':form} 
    return render(request, 'proyecto/cronograma_registrar.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3])
def eliminar_actividad(request, id_act):
    ActividadesCronograma.objects.get(id=id_act).delete()
    return redirect('cronograma_actividad')

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['estudiante','tutor','docente','director','tribunal'])
# def formulario_1(request,id_est):
    # buffer = io.BytesIO()
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    # formulario1(buffer,estudiante)
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename='formulario_1.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3])
def confirmarPaso4(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    if not estudiante.actividad.filter(nombre='tutor acepto'):
        return HttpResponse('error')
    if request.method == 'POST':
        agregarActividadEquipo('imprimir formulario', estudiante.equipo)
        # crear sala de revision perfil
        SalaDocumentoApp.objects.create(
            revisor = estudiante.equipo.tutor.usuario,    
            grupo_revisor = estudiante.equipo.tutor.usuario.groups.get(),
            equipo = estudiante.equipo,
            tipo = 'proyecto',
            )
        SalaDocumentoApp.objects.create(
            revisor = estudiante.grupo_doc.usuario,    
            grupo_revisor = estudiante.grupo_doc.usuario.groups.get(),
            equipo = estudiante.equipo,
            tipo = 'proyecto',
            )
        return redirect('estudiante')
    context = {'grupo': grupo,}
    return render(request, 'proyecto/confirmar_paso.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4])
def paso5(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    tutor = estudiante.equipo.tutor
    docente = estudiante.grupo_doc
    proyecto_grado = ProyectoDeGrado.objects.filter(equipo=estudiante.equipo).exists()
    proyecto = ProyectoDeGrado.objects.filter(equipo=estudiante.equipo)
    # progreso = Progreso.objects.get(usuario=estudiante)
    registro_perfil_existe = RegistroPerfil.objects.filter(equipo=estudiante.equipo).exists()
    # progreso = Progreso.objects.get(usuario=estudiante)
    progreso = progress(estudiante)
    perfil = RegistroPerfil.objects.filter(equipo=estudiante.equipo)
    # nueva app revision
    sala_doc = SalaDocumentoApp.objects.get(equipo=estudiante.equipo, revisor=tutor.usuario, tipo='proyecto')
    if sala_doc.visto_bueno:
        sala_doc = SalaDocumentoApp.objects.get(equipo=estudiante.equipo, revisor=docente.usuario, tipo='proyecto')
    salas_doc = SalaDocumentoApp.objects.filter(equipo=estudiante.equipo, tipo='proyecto')
    context = {'grupo': grupo, 'progreso': progreso,'proyecto_grado':proyecto_grado,
            'proyecto':proyecto,'estudiante':estudiante,
            'salas_doc': salas_doc,
            'sala_doc':sala_doc}
    return render(request, 'proyecto/estudiante_paso5.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4])
def cronograma_control(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    cronograma = ActividadesCronograma.objects.filter(equipo=estudiante.equipo)
    # fecha de registro del cronograma o fecha de registro del proyecto
    fecha = RegistroPerfil.objects.get(equipo=estudiante.equipo).fecha_creacion
    fecha = fecha.astimezone().date()# - timedelta(0)
    # de semanas a dias:
    max_semana = range(1,1+max([n.semana_final for n in cronograma]))
    vector_final = []
    for c in cronograma:
        vector = []
        for n in max_semana:
            if n < c.semana_inicial or n > c.semana_final:
                vector.append(' ')
            else:
                vector.append('*')
        vector_final.append(vector)
    dicc_crono = {}
    for n in range(len(cronograma)):
        dicc_crono[cronograma[n]] = vector_final[n]
    semana_actividad = {}
    for semana in max_semana:
        vec_actividad = []
        for actividad in cronograma:
            if semana >= actividad.semana_inicial and semana <= actividad.semana_final:
                vec_actividad.append(actividad.actividad)
        semana_actividad[semana] = vec_actividad
    # fecha transcurrida desde el inicio
    dias_transcurridos = date.today() - fecha
    # dias_transcurridos = dias_transcurridos #+ timedelta(0)
    # dias a semanas:
    semanas = dias_transcurridos.days // 7# - 1
    num_semana = dias_transcurridos.days // 7 + 1
    dias = dias_transcurridos.days % 7
    dias_transcurridos = dias_transcurridos.days# - 7
    # duracion del proyecto
    semana_total = len(max_semana)
    dia_total = 7*semana_total
    # fecha limite cronograma
    fecha_limite_crono = fecha + timedelta(dia_total)
    dia_restante_crono = fecha_limite_crono - date.today()
    dia_restante_crono = dia_restante_crono.days
    # fecha limite sistema 2 años y medio
    fecha_limite_sistema = fecha + timedelta(365*2.5)
    dia_restante_sistema = fecha_limite_sistema - date.today()
    dia_restante_sistema= dia_restante_sistema.days
    # porcentaje
    por_dia_crono = (dia_restante_crono* 100) / dia_total
    por_dia_sistema = dia_restante_sistema* 100 / (365*2.5)
    por_dia_crono = str(por_dia_crono)
    por_dia_sistema = str(por_dia_sistema)

    dia_retrazo = dia_restante_crono * -1
    por_dia_retrazo = ( dia_restante_crono *-1* 100)/(365*2.5-dia_total) 
    por_dia_retrazo= str(por_dia_retrazo)
    if num_semana <= semana_total:
        actividades = semana_actividad[num_semana]
        limite_cronograma = False
    else:
        actividades = []
        limite_cronograma = True
    # fecha = RegistroCronograma.objects.get(usuario=estudiante).fecha_creacion
    context = {'grupo': grupo, 'cronograma': cronograma, 'fecha': fecha,
            'semanas': semanas, 'dias': dias, 
            'actividades': actividades,
            'dias_transcurridos':dias_transcurridos,
            'fecha_limite_crono':fecha_limite_crono,
            'fecha_limite_sistema':fecha_limite_sistema,
            'dia_restante_crono':dia_restante_crono,
            'dia_restante_sistema':dia_restante_sistema,
            'dia_retrazo':dia_retrazo,
            'semana_tota':semana_total,
            'por_dia_crono':por_dia_crono,
            'por_dia_sistema':por_dia_sistema,
            'por_dia_retrazo':por_dia_retrazo,
            'limite_cronograma':limite_cronograma}
    return render(request, 'proyecto/cronograma_control.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4])
def entregaProyecto(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    estudiante = usuario.datosestudiante
    docente = estudiante.grupo_doc
    tutor = estudiante.tutor
    salas = SalaRevisarProyecto.objects.filter(estudiante_rev=estudiante) 
    dicc_salas = {}
    for sala in salas:
        mensajes_doc = MensajeDocenteRevisarProyecto.objects.filter(sala=sala)
        mensajes_tut = MensajeTutorRevisarProyecto.objects.filter(sala=sala)
        no_visto_docente = 0
        for mensaje_doc in mensajes_doc:
            if not mensaje_doc.visto_estudiante:
                no_visto_docente += 1
        no_visto_tutor = 0
        for mensaje_tut in mensajes_tut:
            if not mensaje_tut.visto_estudiante:
                no_visto_tutor += 1
        dicc_salas[sala] = [no_visto_docente, no_visto_tutor]
    context = {'grupo': grupo,
            'salas':salas,
            'dicc_salas':dicc_salas,
            'estudiante':estudiante}
    return render(request, 'proyecto/entrega_proyecto.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4])
def crearSalaRevisarProyecto(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    estudiante = usuario.datosestudiante
    docente = estudiante.grupo_doc
    tutor = estudiante.tutor
    if request.method == 'POST':
        form = SalaRevisarProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            nombre_sala = request.POST['sala']
            file = form.save(commit=False)
            file.docente_rev = docente
            file.tutor_rev= tutor
            file.estudiante_rev = estudiante
            file.sala = nombre_sala
            file.save()
            return redirect('entrega_proyecto')
            # messages.success(request, 'Se creó la sala revisión con éxito!!!')
    else: 
        form = SalaRevisarProyectoForm
    context = {'grupo': grupo,'form':form,}
    return render(request, 'proyecto/crear_sala_revisar.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','docente','tutor'])
def salaRevisarProyecto(request, pk_sala):
    grupo = request.user.groups.get().name
    usuario = request.user
    info_estu = SalaRevisarProyecto.objects.get(id=pk_sala)
    if grupo == 'docente':
        if request.method == "POST":
            form= MensajeDocenteRevisarProyectoForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.visto_docente = True
                file.save()
        else:
            form= MensajeDocenteRevisarProyectoForm
    elif grupo == 'tutor':
        if request.method == "POST":
            form= MensajeTutorRevisarProyectoForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.visto_tutor = True
                file.save()
        else:
            form= MensajeTutorRevisarProyectoForm()
    mensajes_doc = MensajeDocenteRevisarProyecto.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    mensajes_tut = MensajeTutorRevisarProyecto.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    for mensaje_doc in mensajes_doc:
        mensaje_doc.visto_docente= True
        mensaje_doc.save()
    for mensaje_tut in mensajes_tut:
        mensaje_tut.visto_tutor= True
        mensaje_tut.save()
    context = {'grupo': grupo, 'info_estu':info_estu,
            'form':form,
            'mensajes_doc':mensajes_doc,
            'mensajes_tut':mensajes_tut,
    }
    return render(request, 'proyecto/sala_revisar.html', context)

@login_required(login_url='login')
@permitir_con(pasos=[1,2,3,4])
def salaRevisarProyEstDoc(request, pk_sala):
    grupo = request.user.groups.get().name
    usuario = request.user
    info_estu = SalaRevisarProyecto.objects.get(id=pk_sala)
    if grupo == 'estudiante':
        if request.method == "POST":
            form= MensajeDocenteRevisarProyectoForm(request.POST)
            # print(form)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.visto_estudiante = True
                file.save()
        else:
            form = MensajeDocenteRevisarProyectoForm
    mensajes_doc = MensajeDocenteRevisarProyecto.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    mensajes_tut = MensajeTutorRevisarProyecto.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    for mensaje_doc in mensajes_doc:
        mensaje_doc.visto_estudiante = True
        mensaje_doc.save()
    context = {'grupo': grupo, 'info_estu':info_estu,
            'form':form,
            'mensajes_doc':mensajes_doc,
            'mensajes_tut':mensajes_tut,
            }
    return render(request, 'proyecto/sala_revisar_proy_est_doc.html', context)

@login_required(login_url='login')
@permitir_con(pasos=[1,2,3,4])
def salaRevisarProyEstTut(request, pk_sala):
    grupo = request.user.groups.get().name
    usuario = request.user
    info_estu = SalaRevisarProyecto.objects.get(id=pk_sala)
    if grupo == 'estudiante':
        if request.method == "POST":
            form= MensajeTutorRevisarProyectoForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.visto_estudiante = True
                file.save()
        else:
            form = MensajeTutorRevisarProyectoForm
    mensajes_doc = MensajeDocenteRevisarProyecto.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    mensajes_tut= MensajeTutorRevisarProyecto.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    for mensaje_tut in mensajes_tut:
        mensaje_tut.visto_estudiante = True
        mensaje_tut.save()
    context = {'grupo': grupo, 'info_estu':info_estu,
            'form':form,
            'mensajes_doc':mensajes_doc,
            'mensajes_tut':mensajes_tut,
            }
    return render(request, 'proyecto/sala_revisar_proy_est_tut.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante',])
def reporteCapitulos(request, id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    docReporteCapitulos(buffer, estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte_aceptacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4,5])
def paso6(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    is_nota_tribunal_2 = NotaTribunal.objects.filter(equipo=estudiante.equipo).count() == 2
    vector_sala_doc = SalaDocumentoApp.objects.filter(equipo=estudiante.equipo, tipo='tribunal')
    vec_visto_bueno = [v.visto_bueno for v in vector_sala_doc]
    if vec_visto_bueno == []:
        visto_bueno = False
    else:
        visto_bueno = all(vec_visto_bueno)
    context = {'grupo': grupo, 
            'estudiante': estudiante,
            'salas_doc':vector_sala_doc,
            'is_nota_tribunal_2':is_nota_tribunal_2,
            'visto_bueno':visto_bueno}
    return render(request, 'proyecto/estudiante_paso6.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4,5])
def solicitudTribunal(request, id_est):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    context = {'grupo':grupo,'estudiante':estudiante}
    return render(request, 'proyecto/solicitud_tribunal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4,5])
def crearSalaRevisarTribunal(request,id_trib):
    grupo = request.user.groups.get().name
    usuario = request.user
    estudiante = usuario.datosestudiante
    id_est = estudiante.id
    tribunal = DatosTribunal.objects.get(id=id_trib)
    if request.method == 'POST':
        form = SalaRevisarTribunalForm(request.POST, request.FILES)
        if form.is_valid():
            nombre_sala = request.POST['sala']
            file = form.save(commit=False)
            file.tribunal_rev = tribunal
            file.estudiante_rev = estudiante
            file.sala = nombre_sala
            file.save()
            return redirect('entrega_tribunal', id_est=id_est, id_trib=id_trib)
    else: 
        form = SalaRevisarTribunalForm
    context = {'grupo': grupo,'form':form,}
    return render(request, 'proyecto/crear_sala_revisar.html', context)

@permitir_con(pasos=[1,2,3,4,5])
@login_required(login_url='login')
def salaRevisarEstTrib(request, pk_sala,id_trib):
    grupo = request.user.groups.get().name
    usuario = request.user
    info_estu = SalaRevisarTribunal.objects.get(id=pk_sala)
    estudiante = usuario.datosestudiante
    tribunal = DatosTribunal.objects.get(id=id_trib)
    if grupo == 'estudiante':
        if request.method == "POST":
            form= MensajeTribunalRevisarForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.save()
        else:
            form = MensajeTribunalRevisarForm
    mensajes_trib= MensajeTribunalRevisar.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    for mensaje_trib in mensajes_trib:
        mensaje_trib.visto_estudiante = True
        mensaje_trib.save()
    context = {'grupo': grupo, 'info_estu':info_estu,
            'form':form,
            'estudiante':estudiante,
            'tribunal':tribunal,
            'mensajes_trib':mensajes_trib,
            }
    return render(request, 'proyecto/sala_revisar_est_trib.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','docente','tutor','tribunal'])
def salaRevisarTribunal(request, pk_sala):
    grupo = request.user.groups.get().name
    usuario = request.user
    info_estu = SalaRevisarTribunal.objects.get(id=pk_sala)
    if grupo == 'tribunal':
        if request.method == "POST":
            form= MensajeTribunalRevisarForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.visto_docente = True
                file.save()
        else:
            form= MensajeTribunalRevisarForm
    mensajes_trib = MensajeTribunalRevisar.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    for mensaje_trib in mensajes_trib:
        mensaje_trib.visto_tribunal = True
        mensaje_trib.save()
    context = {'grupo': grupo, 'info_estu':info_estu,
            'form':form,
            'mensajes_trib':mensajes_trib,
    }
    return render(request, 'proyecto/sala_revisar.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
# @permitir_paso6()
@permitir_con(pasos=[1,2,3,4,5])
def entregaTribunal(request, id_trib, id_est):
    grupo = request.user.groups.get().name
    usuario = request.user
    estudiante = usuario.datosestudiante
    docente = estudiante.grupo_doc
    tutor = estudiante.tutor
    tribunal = estudiante.tribunales.get(id=id_trib)
    salas = SalaRevisarTribunal.objects.filter(estudiante_rev=estudiante, tribunal_rev=tribunal) 
    # visto bueno diferente filosofia
    vb_tribunal = False
    for sala in salas:
        if sala.visto_bueno:
            vb_tribunal = sala.visto_bueno
            break
    dicc_salas = {}
    for sala in salas:
        mensajes_trib = MensajeTribunalRevisar.objects.filter(sala=sala)
        no_visto_trib = 0
        for mensaje_trib in mensajes_trib:
            if not mensaje_trib.visto_estudiante:
                no_visto_trib += 1
        dicc_salas[sala] = no_visto_trib
    context = {'grupo': grupo,
            'salas':salas,
            'dicc_salas':dicc_salas,
            'tribunal':tribunal,
            'vb_tribunal':vb_tribunal,
            'estudiante':estudiante}
    return render(request, 'proyecto/entrega_tribunal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4,5])
def registroProyectoTribunal(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    form = RegistroProyectoTribunalForm
    if request.method == 'POST':
        form = RegistroProyectoTribunalForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.equipo = estudiante.equipo
            form.save()
            agregarActividadEquipo("registro proyecto tribunal", estudiante.equipo)
            agregarActividadEquipo("fecha defensa", estudiante.equipo)
            agregarActividadEquipo("defensa realizada", estudiante.equipo)
        return redirect('paso6')
    context = {'grupo': grupo,'form':form,}
    return render(request, 'proyecto/registro_proyecto_tribunal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4,5])
def ver_proyecto_tribunal(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    notas_tribunales = NotaTribunal.objects.filter(equipo=estudiante.equipo)
    proyecto = RegistroProyectoTribunal.objects.get(equipo=estudiante.equipo)
    equipo = estudiante.equipo
    context = {'grupo': grupo,'proyecto':proyecto,'estudiante':estudiante,
            'notas_tribunales':notas_tribunales,'equipo':equipo}
    return render(request, 'proyecto/ver_proyecto_tribunal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4])
def registroProyecto(request):
    grupo = request.user.groups.get().name
    equipo = request.user.datosestudiante.equipo
    form = ProyectoDeGradoForm
    if request.method == 'POST':
        form = ProyectoDeGradoForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.equipo = equipo
            form.save()
            agregarActividadEquipo('registro proyecto', equipo)
        return redirect('paso5')
    context = {'grupo': grupo,'form':form,}
    return render(request, 'proyecto/registro_proyecto.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4])
def ver_proyecto_grado(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    proyecto = ProyectoDeGrado.objects.get(equipo=estudiante.equipo)
    context = {'grupo': grupo,'proyecto':proyecto}
    return render(request, 'proyecto/ver_proyecto_grado.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente'])
def calificarProyecto(request, pk):
    grupo = request.user.groups.get().name
    usuario = request.user.datosdocente
    estudiante = DatosEstudiante.objects.get(id=pk)
    equipo = estudiante.equipo
    if request.method == 'POST':
        form = CalificarProyectoForm(request.POST)
        nota1 = request.POST['nota1']
        nota2 = request.POST['nota2']
        nota3 = request.POST['nota3']
        nota4 = request.POST['nota4']
        proyecto = ProyectoDeGrado.objects.get(equipo=equipo)
        proyecto.nota_tiempo_elaboracion = nota1
        proyecto.nota_expos_seminarios = nota2
        proyecto.nota_informes_trabajo = nota3
        proyecto.nota_cumplimiento_cronograma = nota4
        proyecto.calificacion = int(nota1)+int(nota2)+int(nota3)+int(nota4)
        proyecto.save()
        agregarActividadEquipo('nota docente proyecto', equipo)
        return redirect('progreso_estudiante',pk=equipo.pk)
    else: 
        form = CalificarProyectoForm
    context = {'grupo': grupo,'estudiante':estudiante, 'form': form}
    return render(request, 'proyecto/calificar_proyecto.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tribunal'])
def calificarProyectoTribunal(request, pk):
    grupo = request.user.groups.get().name
    tribunal = request.user.datostribunal
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    equipo = get_object_or_404(Equipo, id=pk)
    # nota_docente = ProyectoDeGrado.objects.get(usuario=estudiante).calificacion
    form = CalificarProyectoTribunalForm
    if NotaTribunal.objects.filter(tribunal=tribunal, equipo=equipo).exists():
        return HttpResponse('error')
    if request.method == 'POST':
        form = CalificarProyectoTribunalForm(request.POST)
        if form.is_valid():
            form.instance.equipo = equipo
            form.instance.tribunal = tribunal
            form.save()
            if actividadRealizadaEstudiante("nota tribunal 1", equipo.datosestudiante_set.first()):
                agregarActividadEquipo("nota tribunal 2", equipo)
            else:
                agregarActividadEquipo("nota tribunal 1", equipo)
            proyecto = equipo.registroproyectotribunal
            promedio = form.cleaned_data.get('nota') / 2
            proyecto.nota = proyecto.nota + promedio
            proyecto.save()
            equipo.nota_final = proyecto.nota + equipo.proyectodegrado.calificacion
            equipo.save()
        return redirect('progreso_estudiante',pk=pk)
    context = {'grupo': grupo,'equipo':equipo, 'form': form}
    return render(request, 'proyecto/calificar_proyecto_tribunal.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3])
def confirmarPaso6(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    if not actividadRealizadaEstudiante('nota tribunal 2',estudiante):
        return HttpResponse('error')
    if request.method == 'POST':
        agregarActividadEquipo('documentacion final', estudiante.equipo)
        agregarActividadEquipo('conclusion', estudiante.equipo)
        estudiante.equipo.fecha_conclusion = date.today()
        estudiante.equipo.save()
        return redirect('estudiante')
    context = {'grupo': grupo,}
    return render(request, 'proyecto/confirmar_paso.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente'])
def solicitarTribunalDocente(request, pk):
    grupo = request.user.groups.get().name
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    equipo = Equipo.objects.get(id=pk)
    if request.method == 'POST':
        confirmar = request.POST['confirmar']
        if confirmar == 'si':
            equipo.solicitud_tribunal_docente = True
            equipo.save()
            agregarActividadEquipo("solicitud de tribunal", equipo)
        return redirect('progreso_estudiante', pk=pk)
    context = {'grupo': grupo,'equipo':equipo}
    return render(request, 'proyecto/confirmar_sol_trib.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2,3,4,5])
def ultimosFormularios(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    context = {'grupo': grupo,'estudiante':estudiante}
    return render(request, 'proyecto/ultimos_formularios.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor'])
def materialParaEst(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    form = MaterialDocenteForm
    if request.method == 'POST':
        form = MaterialDocenteForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.propietario = usuario
            file.save()
            return redirect('material_para_estudiante')
    materiales = MaterialDocente.objects.filter(propietario=request.user)
    context = {'grupo': grupo,'form':form, 'materiales':materiales}
    return render(request, 'proyecto/material_para_estudiante.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor'])
def eliminarMaterialParaEst(request, id_material):
    material = get_object_or_404(MaterialDocente, id=id_material)
    id_usuario = material.propietario.id
    if request.method == 'POST':
        material.delete()
        return redirect('material_para_estudiante')
    context = {'material':material}
    return render(request, 'proyecto/eliminar_material.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
# def formulario_2(request, id_est):
    # buffer = io.BytesIO()
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    # proyecto = ProyectoDeGrado.objects.get(usuario=estudiante)
    # # lo siguiente hay que hagregar de alguna forma a la base de datos
    # info_estu = [
            # estudiante.__str__(),
            # estudiante.tutor.__str__(),
            # estudiante.grupo_doc.__str__(),
            # proyecto.titulo,
            # estudiante.mencion,
            # proyecto.resumen,
            # proyecto.fecha_creacion,
            # ]
    # formulario2(buffer,estudiante)
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename='formulario_2.pdf')

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
# # @permitir_paso6()
# def formulario_3(request, id_est):
    # buffer = io.BytesIO()
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    # proyecto = ProyectoDeGrado.objects.get(usuario=estudiante)
    # # lo siguiente hay que hagregar de alguna forma a la base de datos
    # formulario3(buffer,estudiante,proyecto)
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename='formulario_3.pdf')

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['estudiante','tutor','docente'])
# # @permitir_paso6()
# def auspicioF3(request, id_est):
    # grupo = request.user.groups.get().name
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    # if not Auspicio.objects.filter(usuario=estudiante).exists():
        # Auspicio.objects.create(usuario=estudiante)
    # auspicio_est = Auspicio.objects.get(usuario=estudiante)
    # form = AuspicioForm(instance=auspicio_est)
    # if request.method == 'POST':
        # form = AuspicioForm(request.POST, instance=auspicio_est)
        # if form.is_valid():
            # form.save()
            # return redirect('paso6')
    # context = {'grupo': grupo,'form':form,'estudiante':estudiante}
    # return render(request, 'proyecto/auspicio_f3.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
# def formulario_4(request, id_est):
    # buffer = io.BytesIO()
    # estudiante = DatosEstudiante.objects.get(id=id_est)
    # proyecto = ProyectoDeGrado.objects.get(usuario=estudiante)
    # # lo siguiente hay que hagregar de alguna forma a la base de datos
    # extension = 'L.P.'
    # cargo = 'director'
    # lugar = 'instituto de electrónica aplicada'
    # institucion = 'facultad de ingeniería'
    # formulario4(buffer,estudiante, proyecto)
    # buffer.seek(0)
    # return FileResponse(buffer, as_attachment=True, filename='formulario_4.pdf')

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['estudiante'])
# def confirmarPaso1(request):
    # grupo = request.user.groups.get().name
    # estudiante = request.user.datosestudiante
    # progreso = Progreso.objects.get(usuario=estudiante)
    # if request.method == 'POST':
        # confirmar = request.POST['confirmar']
        # confirmar = int(confirmar)
        # if 1 <= confirmar < 14:
            # progreso.nivel = 14
        # if 14 <= confirmar < 21:
            # progreso.nivel = 21
        # if 35 <= confirmar < 64:
            # progreso.nivel = 64
            # # crear sala de revision perfil
            # SalaDocumentoApp.objects.create(
                # revisor = estudiante.tutor.usuario,    
                # grupo_revisor = estudiante.tutor.usuario.groups.get(),
                # estudiante = estudiante,
                # tipo = 'proyecto',
                # )
            # SalaDocumentoApp.objects.create(
                # revisor = estudiante.grupo_doc.usuario,    
                # grupo_revisor = estudiante.grupo_doc.usuario.groups.get(),
                # estudiante = estudiante,
                # tipo = 'proyecto',
                # )
        # progreso.save()
        # return redirect('estudiante')
    # context = {'grupo': grupo, 'progreso': progreso}
    # return render(request, 'proyecto/confirmar_paso.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['estudiante'])
# # @permitir_paso5()
# @permitir_con(pasos=[1,2,3,4])
# def confirmarPaso5(request):
    # grupo = request.user.groups.get().name
    # estudiante = request.user.datosestudiante
    # progreso = Progreso.objects.get(usuario=estudiante)
    # if request.method == 'POST':
        # confirmar = request.POST['confirmar']
        # confirmar = int(confirmar)
        # # if confirmar < 81 and confirmar >= 69:
        # if 64 <= confirmar < 86:
            # progreso.nivel = 86
        # progreso.save()
        # return redirect('estudiante')
    # context = {'grupo': grupo, 'progreso': progreso}
    # return render(request, 'proyecto/confirmar_paso.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['estudiante'])
# # @permitir_paso6()
# @permitir_con(pasos=[1,2,3,4,5])
# def confirmarPaso6(request):
    # grupo = request.user.groups.get().name
    # estudiante = request.user.datosestudiante
    # progreso = Progreso.objects.get(usuario=estudiante)
    # if request.method == 'POST':
        # confirmar = request.POST['confirmar']
        # confirmar = int(confirmar)
        # # if confirmar < 100 and confirmar >= 81:
        # if 86 <= confirmar < 100:
            # progreso.nivel = 100
            # # agregando a lista de titulados
            # DatosEstudianteTitulado.objects.create(
                    # correo = estudiante.correo,
                    # nombre = estudiante.nombre,
                    # apellido = estudiante.apellido,
                    # carnet = estudiante.carnet,
                    # extension = estudiante.extension,
                    # registro_uni = estudiante.registro_uni,
                    # celular = estudiante.celular, 
                    # mencion = estudiante.mencion,
                    # tutor = estudiante.tutor,
                    # docente = estudiante.grupo_doc,
                    # imagen_perfil =estudiante.imagen_perfil,
                    # )
        # progreso.save()
        # return redirect('estudiante')
    # context = {'grupo': grupo, 'progreso': progreso}
    # return render(request, 'proyecto/confirmar_paso.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente'])
def perfilCorregido (request, id_sala):
    grupo = request.user.groups.get().name
    sala = SalaRevisar.objects.get(id=id_sala)
    id_est = sala.estudiante_rev.id
    if grupo == 'tutor':
        form = PerfilCorregidoTutorForm(instance=sala)
        if request.method == 'POST':
            form = PerfilCorregidoTutorForm(request.POST, request.FILES, instance=sala)
            if form.is_valid():
                form.save()
                return redirect('progreso_estudiante', pk_est=id_est)
    if grupo == 'docente':
        form = PerfilCorregidoDocenteForm(instance=sala)
        if request.method == 'POST':
            form = PerfilCorregidoDocenteForm(request.POST, request.FILES, instance=sala)
            if form.is_valid():
                form.save()
                return redirect('progreso_estudiante', pk_est=id_est)
        # return redirect('paso5')
    context = {'grupo': grupo,'form':form,'sala':sala}
    return render(request, 'proyecto/proyecto_corregido.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente'])
def proyectoCorregido (request, id_sala):
    grupo = request.user.groups.get().name
    sala = SalaRevisarProyecto.objects.get(id=id_sala)
    id_est = sala.estudiante_rev.id
    if grupo == 'tutor':
        form = ProyectoCorregidoTutorForm(instance=sala)
        if request.method == 'POST':
            form = ProyectoCorregidoTutorForm(request.POST, request.FILES, instance=sala)
            if form.is_valid():
                form.save()
                return redirect('progreso_estudiante', pk_est=id_est)
    if grupo == 'docente':
        form = ProyectoCorregidoDocenteForm(instance=sala)
        if request.method == 'POST':
            form = ProyectoCorregidoDocenteForm(request.POST, request.FILES, instance=sala)
            if form.is_valid():
                form.save()
                return redirect('progreso_estudiante', pk_est=id_est)
        # return redirect('paso5')
    context = {'grupo': grupo,'form':form,'sala':sala}
    return render(request, 'proyecto/proyecto_corregido.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['director','administrador',])
def listaTribunales(request):
    grupo = request.user.groups.get().name
    tribunales = DatosTribunal.objects.all().order_by('apellido')
    context = {'grupo':grupo, 'tribunales':tribunales}
    return render(request, 'proyecto/lista_tribunales.html', context)

def error(request):
    return render(request, 'proyecto/error_pagina.html')

