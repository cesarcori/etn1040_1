from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from .decorators import unauthenticated_user, allowed_users, admin_only, permitir_paso1
from .decorators import *
from .forms import *
from .models import *
from .cartas import *
from .reportes import *
from .formularios import *
from .funciones import *

from random import randint
from datetime import timedelta

# busqueda
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords

# import nltk
# from pandas import read_csv


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
            # elif DatosEstudiante.objects.filter(usuario=usuario).exists():
                # messages.info(request, 
            # 'No se envió la solicitud, un estudiante usa este mismo nombre de usuario')
            elif DatosEstudiante.objects.filter(correo=correo).exists():
                messages.info(request, 
            'No se envió la solicitud, un estudiante usa este mismo correo electrónico')
            elif DatosEstudiante.objects.filter(carnet=carnet).exists():
                messages.info(request, 
            'No se envió la solicitud, un estudiante usa este mismo número de carnet')
            elif DatosEstudiante.objects.filter(registro_uni=registro_uni).exists():
                messages.info(request, 
            'No se envió la solicitud, un estudiante usa este mismo número de \
            registro universitario')
            else:
                SolicitudInvitado.objects.create(
                        usuario = usuario,
                        correo = correo,
                        nombre = nombre,
                        apellido = apellido,
                        carnet = carnet,
                        extension = extension,
                        registro_uni = registro_uni,
                        celular = celular,
                        mencion = mencion,
                        password = password
                        )
                messages.success(request, 'La solicitud se envió con exito!!!')
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
    info = 'No se realizó ninguna acción'
    if request.method == 'POST':
        usuario_habi = request.POST.get('habilitar')
        usuario_elim = request.POST.get('eliminar') 
        if usuario_habi != None:
            info_usuario = SolicitudInvitado.objects.get(pk=usuario_habi)
            info = 'Se habilito al estudiante: ' + info_usuario.apellido + ' ' \
            + info_usuario.nombre
            # sorteo de grupo_docente
            mencion = info_usuario.mencion
            doc_mencion = DatosDocente.objects.filter(mencion=mencion)
            cantidad_est1 = doc_mencion[0].datosestudiante_set.count()
            cantidad_est2 = doc_mencion[1].datosestudiante_set.count()
            if cantidad_est1 == cantidad_est2:
                sorteo = randint(0,1)
                docente_asignado = doc_mencion[sorteo]
            elif cantidad_est1 < cantidad_est2:
                docente_asignado = doc_mencion[0]
            else:
                docente_asignado = doc_mencion[1]

            docente = doc_mencion[0]                   
            # creacion del usuario
            User.objects.create_user(
                    username = info_usuario.usuario,
                    email = info_usuario.correo,
                    first_name = info_usuario.nombre,
                    last_name = info_usuario.apellido,
                    password = info_usuario.password,
                    )

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
            Progreso.objects.create(
                    usuario = estudiante,
                    nivel = 1
                    )
            # creacion de salas docente-estudiante
            id_docente = str(DatosEstudiante.objects.last().grupo_doc.usuario_id)
            id_estudiante = str(DatosEstudiante.objects.last().usuario_id)
            nombre_sala = id_docente + id_estudiante
            Sala.objects.create(nombre_sala = nombre_sala)
            # creacion de grupo
            group = Group.objects.get(name='estudiante')
            user = User.objects.get(username=info_usuario.usuario)
            user.groups.add(group)
            
            SolicitudInvitado.objects.get(pk=usuario_habi).delete()

        elif usuario_elim != None:
            info_usuario = SolicitudInvitado.objects.get(pk=usuario_elim)
            info = 'Se eliminó al estudiante: ' + info_usuario.apellido + ' ' \
            + info_usuario.nombre
            SolicitudInvitado.objects.get(pk=usuario_elim).delete()
    solicitudes = SolicitudInvitado.objects.all()
    aviso = 'Tiene: ' + str(solicitudes.count()) + ' solicitudes'
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
    datos_est = request.user.datosdocente.datosestudiante_set.all().order_by('apellido')
    context = {'datos_est':datos_est,'grupo':grupo}
    return render(request, 'proyecto/docente.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor'])
def tutor(request):
    grupo = 'tutor'
    datos_est = request.user.datostutor.datosestudiante_set.all().order_by('apellido')
    context = {'datos_est':datos_est,'grupo':grupo}
    return render(request, 'proyecto/tutor.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['director'])
def director(request):
    grupo = 'director'
    datos_est = DatosEstudiante.objects.all().order_by('apellido')
    context = {'datos_est':datos_est,'grupo':grupo}
    return render(request, 'proyecto/director.html', context)

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
def solicitudTutoria(request, id_est):
    grupo = 'tutor'
    estudiante = DatosEstudiante.objects.get(id=id_est)
    aceptar = 'no'
    rechazar = 'no'
    if request.method == 'POST':
        aceptar = request.POST.get('confirmar')
        rechazar = request.POST.get('rechazar') 
    if aceptar == 'si':
        estudiante.tutor_acepto = True
        estudiante.save()
        progreso = Progreso.objects.get(usuario=estudiante)
        progreso.nivel = 35
        progreso.save()
        return redirect('tutor')
    if rechazar == 'si':
        estudiante.tutor = None
        estudiante.save()
        return redirect('tutor')
    context = {'grupo':grupo,'estudiante':estudiante}
    return render(request, 'proyecto/solicitud_tutoria.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def estudiante(request):
    grupo = 'estudiante'
    estudiante = request.user.datosestudiante
    # si se pasa del tiempo se elimina del sistema
    # cronograma_existe = ActividadesCronograma.objects.filter(usuario=estudiante).exists()
    # if cronograma_existe:
        # cronograma = ActividadesCronograma.objects.filter(usuario=estudiante)
            # # fecha de registro del cronograma o fecha de registro del proyecto
        # fecha = RegistroPerfil.objects.get(usuario=estudiante).fecha_creacion
            # # fecha limite sistema 2 años y medio
        # # prueba modificar el 0 del delta para eliminar al usuario
        # fecha = fecha.date()#-timedelta(0)
        # fecha_limite_sistema = fecha+ timedelta(365*2.5)
        # dia_restante_sistema = fecha_limite_sistema - date.today()
        # dia_restante_sistema = dia_restante_sistema.days
        # # fecha transcurrida desde el inicio
        # dias_transcurridos = date.today() - fecha
        # dias_transcurridos = dias_transcurridos + timedelta(0)
        # # dias a semanas:
        # semanas = dias_transcurridos.days // 7# - 1
        # num_semana = dias_transcurridos.days // 7 + 1
        # dias = dias_transcurridos.days % 7
        # dias_transcurridos = dias_transcurridos.days# - 7
        # # duracion del proyecto
        # max_semana = range(1,1+max([n.semana_final for n in cronograma]))
        # semana_total = len(max_semana)
        # dia_total = 7*semana_total
        # # fecha limite cronograma
        # fecha_limite_crono = fecha + timedelta(dia_total)
        # dia_restante_crono = fecha_limite_crono - date.today()
        # dia_restante_crono = dia_restante_crono.days
        # # fecha limite sistema 2 años y medio
        # fecha_limite_sistema = fecha + timedelta(365*2.5)
        # dia_restante_sistema = fecha_limite_sistema - date.today()
        # dia_restante_sistema= dia_restante_sistema.days
        # # porcentaje
        # por_dia_crono = (dia_restante_crono* 100) / dia_total
        # por_dia_sistema = dia_restante_sistema* 100 / (365*2.5)
        # por_dia_crono = str(por_dia_crono)
        # por_dia_sistema = str(por_dia_sistema)

        # dia_retrazo = dia_restante_crono * -1
        # por_dia_retrazo = ( dia_restante_crono *-1* 100)/(365*2.5-dia_total) 
        # por_dia_retrazo= str(por_dia_retrazo)

        # if num_semana <= semana_total:
            # limite_cronograma = False
        # else:
            # actividades = []
            # limite_cronograma = True
        # if dia_restante_sistema <= -1 and progreso < 100:
            # estudiante.usuario.delete()
            # print('Se jodio')
            # return HttpResponse("Han pasado 2 años y medio, Fuiste Eliminado del sistema.")
    # else:
        # dia_restante_crono = ''
        # dia_restante_sistema = ''
        # dia_retrazo = ''
        # semana_total = ''
        # por_dia_crono = ''
        # por_dia_sistema = ''
        # por_dia_retrazo = ''
        # limite_cronograma = ''

    context_aux = infoCronograma(estudiante.id)
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
            mencion = estudiante.mencion
            doc_mencion = DatosDocente.objects.filter(mencion=mencion)
            cantidad_est1 = doc_mencion[0].datosestudiante_set.count()
            cantidad_est2 = doc_mencion[1].datosestudiante_set.count()
            if cantidad_est1 == cantidad_est2:
                sorteo = randint(0,1)
                docente_asignado = doc_mencion[sorteo]
            elif cantidad_est1 < cantidad_est2:
                docente_asignado = doc_mencion[0]
            else:
                docente_asignado = doc_mencion[1]
            docente = doc_mencion[0]                   
            # guardar docente
            estudiante.grupo_doc = docente
            estudiante.save()
            # creacion de salas docente-estudiante
            id_docente = estudiante.grupo_doc.usuario_id.__str__()
            id_estudiante = estudiante.usuario_id.__str__()
            nombre_sala = id_docente + id_estudiante
            Sala.objects.create(nombre_sala = nombre_sala)
            return redirect('estudiante')
        return render(request, 'proyecto/sorteo_docente.html')
    else:
        if Progreso.objects.filter(usuario=estudiante).exists():
            progreso = Progreso.objects.get(usuario=estudiante).nivel
        else:
            progreso = 1
        context = {'grupo': grupo,'progreso':progreso, 'estudiante':estudiante,}
        context = {**context, **context_aux}
        return render(request, 'proyecto/estudiante.html', context)

@login_required(login_url='login')
def perfilUsuarios(request):
    grupo = request.user.groups.get().name
    context = {'grupo': grupo}
    return render(request, 'proyecto/perfil.html', context)

@login_required(login_url='login')
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
                return redirect('perfil')
    if grupo == 'estudiante':
        estudiante = usuario.datosestudiante
        form = DatosEstudianteForm(instance=estudiante)
        if request.method == "POST":
            form = DatosEstudianteForm(request.POST, request.FILES, instance=estudiante)
            print(form.instance.celular)
            print(form.instance.imagen_perfil)
            if form.is_valid():
                form.save()
                usuario.save()
                return redirect('perfil')
    if grupo == 'administrador':
        administrador = usuario.datosadministrador
        form = DatosAdministradorForm(instance=administrador)
        if request.method == "POST":
            form = DatosAdministradorForm(request.POST, request.FILES, instance=administrador)
            if form.is_valid():
                form.save()
                return redirect('perfil')
    if grupo == 'director':
        director = usuario.datosdirector
        form = DatosDirectorForm(instance=director)
        if request.method == "POST":
            form = DatosDirectorForm(request.POST, request.FILES, instance=director)
            if form.is_valid():
                form.save()
                return redirect('perfil')
    context = {'grupo': grupo,'form':form}
    return render(request, 'proyecto/editar_perfil.html', context)

@login_required(login_url='login')
def editarPassword(request):
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
    context = {'form':form}
    return render(request, 'proyecto/editar_password.html', context)

@login_required(login_url='login')
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
    if request.user.datosestudiante.tutor == None:
        tutor = None
    else:
        tutor = request.user.datosestudiante.tutor.usuario
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
@allowed_users(allowed_roles=['docente','tutor','administrador','director'])
def enlaceEstudiante(request, pk_est):
    grupo = str(request.user.groups.get())
    estudiante = DatosEstudiante.objects.get(id=pk_est)
    if grupo=='administrador' or grupo=='director':
        context = {'grupo': grupo,'estudiante':estudiante,}
        return render(request, 'proyecto/enlace_estudiante.html', context)
    elif grupo == 'docente':
        # evita que se un docente consulte otros estudiantes
        existe_est = request.user.datosdocente.datosestudiante_set.filter(id=pk_est).exists()
        if existe_est:
            context = {'grupo': grupo,'estudiante':estudiante,}
            return render(request, 'proyecto/enlace_estudiante.html', context)
        else:
            return redirect('error_pagina')
    else:           
        existe_est = request.user.datostutor.datosestudiante_set.filter(id=pk_est).exists()
        if existe_est:
            context = {'grupo': grupo,'estudiante':estudiante,}
            return render(request, 'proyecto/enlace_estudiante.html', context)
        else:
            return redirect('error_pagina')

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador','director'])
def enlaceEstudianteTitulado(request, id_est_tit):
    grupo = request.user.groups.get().name
    estudiante = DatosEstudianteTitulado.objects.get(id=id_est_tit)
    if grupo=='administrador' or grupo=='director':
        context = {'grupo': grupo,'estudiante':estudiante,}
        return render(request, 'proyecto/enlace_estudiante_titulado.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','administrador','docente','tutor','director'])
def reporteEstudiante(request, id_est):
    grupo = request.user.groups.get().name
    estudiante = DatosEstudiante.objects.get(id=id_est)
    if estudiante.progreso.nivel == 1:
        pasos = {
                }
        pasos_falta = {
                'Paso 1':['Conocimiento de Reglamentos de Proyecto de Grado',
                        'Revisión y estudio del material compartido por Docente'],
                'Paso 2':['Búsqueda de Proyectos de Grado'],
                'Paso 3':['Asignación de Tutor de Proyecto de Grado',
                        'Carta aceptación de Tutoría'],
                'Paso 4':['Entrega y revisión de Perfil de Proyecto de Grado',
                        'Registro de Perfil de Proyecto de Grado',
                        'Registro de Cronograma de Proyecto de Grado',
                        'Formulario 1'],
                'Paso 5':['Cumplir con el cronograma',
                        'Revisión del Proyecto de Grado',
                        'Registro del Proyecto de Grado',],
                'Paso 6':['Carta de Conclusión',
                    'Gegeración de los 3 formularios']
                }
    if estudiante.progreso.nivel > 1:
        pasos = {'Paso 1':['Conocimiento de Reglamentos de Proyecto de Grado',
                        'Revisión y estudio del material compartido por Docente'],
                }
        pasos_falta = {
                'Paso 2':['Búsqueda de Proyectos de Grado'],
                'Paso 3':['Asignación de Tutor de Proyecto de Grado',
                        'Carta aceptación de Tutoría'],
                'Paso 4':['Entrega y revisión de Perfil de Proyecto de Grado',
                        'Registro de Perfil de Proyecto de Grado',
                        'Registro de Cronograma de Proyecto de Grado',
                        'Formulario 1'],
                'Paso 5':['Cumplir con el cronograma',
                        'Revisión del Proyecto de Grado',
                        'Registro del Proyecto de Grado',],
                'Paso 6':['Carta de Conclusión',
                    'Gegeración de los 3 formularios']
                }
    if estudiante.progreso.nivel > 14:
        pasos['Paso 2'] = ['Búsqueda de Proyectos de Grado']
        del pasos_falta['Paso 2']
    if estudiante.progreso.nivel > 21:
        pasos['Paso 3'] = ['Asignación de Tutor de Proyecto de Grado',
                        'Carta aceptación de Tutoría']
        del pasos_falta['Paso 3']
    if estudiante.progreso.nivel > 35:
        pasos['Paso 4'] = ['Entrega y revisión de Perfil de Proyecto de Grado',
                        'Registro de Perfil de Proyecto de Grado',
                        'Registro de Cronograma de Proyecto de Grado',
                        'Formulario 1']
        del pasos_falta['Paso 4']
    if estudiante.progreso.nivel > 64:
        pasos['Paso 5'] = ['Cumplir con el cronograma',
                        'Revisión del Proyecto de Grado',
                        'Registro del Proyecto de Grado',]
        del pasos_falta['Paso 5']
    if estudiante.progreso.nivel > 86:
        pasos['Paso 6'] = ['Carta de Conclusión',
                    'Gegeración de los 3 formularios']
        del pasos_falta['Paso 6']
    context = {'grupo':grupo,'estudiante':estudiante, 'pasos':pasos, 'pasos_falta':pasos_falta}
    return render(request, 'proyecto/reporte_estudiante.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','administrador','docente','tutor','director'])
def imprimirReporteEstudiante(request, id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    usuario_solicitante = request.user
    docReporteEstudiante(buffer, estudiante, usuario_solicitante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_aceptacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor','administrador','director'])
def progresoEstudiante(request, pk_est):
    grupo = str(request.user.groups.get())
    estudiante = DatosEstudiante.objects.get(id=pk_est)
    progreso = Progreso.objects.get(usuario=estudiante).nivel
    if ProyectoDeGrado.objects.filter(usuario=estudiante).exists():
        proyecto = ProyectoDeGrado.objects.get(usuario=estudiante)
        calificacion = proyecto.calificacion
    else:
        proyecto = None
        calificacion = None
    # cronograma informacion
    context_aux = infoCronograma(estudiante.id)
    if not isinstance(context_aux, dict):
        context_aux = {}
        mensaje = infoCronograma(estudiante.id)
        return HttpResponse(mensaje)
    if grupo == 'docente':
        # evita que se un docente consulte otros estudiantes
        existe_est = request.user.datosdocente.datosestudiante_set.filter(id=pk_est).exists()
        if existe_est:
            info_estu = SalaRevisar.objects.filter(estudiante_rev=estudiante)
            salas = SalaRevisar.objects.filter(estudiante_rev=estudiante) 
            info_estu_proy = SalaRevisarProyecto.objects.filter(estudiante_rev=estudiante)
            salas_proy = SalaRevisarProyecto.objects.filter(estudiante_rev=estudiante) 
            # para que salga notificacion perfil
            dicc_salas = {}
            for sala in salas:
                mensajes_doc = MensajeDocenteRevisar.objects.filter(sala=sala)
                no_visto= 0
                for mensaje_doc in mensajes_doc:
                    if not mensaje_doc.visto_docente:
                        no_visto += 1
                dicc_salas[sala] = no_visto
            # para que salga notificacion proyecto
            dicc_salas_proy = {}
            for sala in salas_proy:
                mensajes_doc = MensajeDocenteRevisarProyecto.objects.filter(sala=sala)
                no_visto= 0
                for mensaje_doc in mensajes_doc:
                    if not mensaje_doc.visto_docente:
                        no_visto += 1
                dicc_salas_proy[sala] = no_visto
            context = {'grupo': grupo,'estudiante':estudiante,
                    'progreso':progreso,
                    'info_estu':info_estu,
                    'salas':salas,
                    'dicc_salas':dicc_salas,
                    'dicc_salas_proy':dicc_salas_proy,
                    'info_estu_proy':info_estu_proy,
                    'salas_proy':salas_proy,
                    'proyecto': proyecto,
                    'calificacion': calificacion,
                    }
            context = {**context_aux, **context}
            return render(request, 'proyecto/progreso_estudiante.html', context)
        else:
            return redirect('error_pagina')
    elif grupo== 'tutor':
        existe_est = request.user.datostutor.datosestudiante_set.filter(id=pk_est).exists()
        if existe_est:
            info_estu = SalaRevisar.objects.filter(estudiante_rev=estudiante)
            salas = SalaRevisar.objects.filter(estudiante_rev=estudiante) 
            info_estu_proy = SalaRevisarProyecto.objects.filter(estudiante_rev=estudiante)
            salas_proy = SalaRevisarProyecto.objects.filter(estudiante_rev=estudiante) 
            # para que salga notificacion
            dicc_salas = {}
            for sala in salas:
                mensajes_tut= MensajeTutorRevisar.objects.filter(sala=sala)
                no_visto= 0
                for mensaje_tut in mensajes_tut:
                    if not mensaje_tut.visto_tutor:
                        no_visto += 1
                dicc_salas[sala] = no_visto
            # para que salga notificacion proyecto
            dicc_salas_proy = {}
            for sala in salas_proy:
                mensajes_tut= MensajeTutorRevisarProyecto.objects.filter(sala=sala)
                no_visto= 0
                for mensaje_tut in mensajes_tut:
                    if not mensaje_tut.visto_tutor:
                        no_visto += 1
                dicc_salas_proy[sala] = no_visto
            context = {'grupo': grupo,'estudiante':estudiante,
                    'progreso':progreso,
                    'info_estu':info_estu,
                    'salas':salas,
                    'dicc_salas':dicc_salas,
                    'dicc_salas_proy':dicc_salas_proy,
                    'info_estu_proy':info_estu_proy,
                    'salas_proy':salas_proy,
                    'proyecto': proyecto,
                    'calificacion': calificacion,
                    }
            context = {**context_aux, **context}
            return render(request, 'proyecto/progreso_estudiante.html', context)
        else:
            return redirect('error_pagina')
    elif grupo== 'director':
        existe_est = DatosEstudiante.objects.filter(id=pk_est).exists()
        if existe_est:
            context = {'grupo': grupo,'estudiante':estudiante,
                    'progreso':progreso,
                    'proyecto': proyecto,
                    'calificacion': calificacion,
                    }
            context = {**context_aux, **context}
            return render(request, 'proyecto/progreso_estudiante.html', context)
        else:
            return redirect('error_pagina')

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor'])
def vistoBuenoPerfil(request, id_est):
    grupo = request.user.groups.get().name
    estudiante = DatosEstudiante.objects.get(id=id_est)
    visto_bueno = 'no'
    if request.method == 'POST':
        visto_bueno = request.POST['visto_bueno']
    if visto_bueno == 'si':
        if grupo == 'docente':
            estudiante.vb_perfil_docente = True
        else:
            estudiante.vb_perfil_tutor = True
        estudiante.save()
        return redirect('progreso_estudiante',pk_est=id_est)
    context = {'grupo': grupo}
    return render(request, 'proyecto/visto_bueno_perfil.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor'])
def vistoBuenoProyecto(request, id_est):
    grupo = request.user.groups.get().name
    estudiante = DatosEstudiante.objects.get(id=id_est)
    visto_bueno = 'no'
    if request.method == 'POST':
        visto_bueno = request.POST['visto_bueno']
    if visto_bueno == 'si':
        if grupo == 'docente':
            estudiante.vb_proyecto_docente = True
        else:
            estudiante.vb_proyecto_tutor = True
        estudiante.save()
        return redirect('progreso_estudiante',pk_est=id_est)
    context = {'grupo': grupo}
    return render(request, 'proyecto/visto_bueno_proyecto.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','administrador','director'])
def enlaceDocente(request, pk_doc):
    grupo = request.user.groups.get().name
    docente = DatosDocente.objects.get(id=pk_doc)
    if grupo == 'administrador':
        estudiantes = docente.datosestudiante_set.all()
        context = {'grupo': grupo, 'estudiantes':estudiantes, 'docente':docente}
        return render(request, 'proyecto/enlace_docente.html', context)
    if grupo == 'director':
        estudiantes = docente.datosestudiante_set.all()
        context = {'grupo': grupo, 'estudiantes':estudiantes, 'docente':docente}
        return render(request, 'proyecto/enlace_docente.html', context)
    elif grupo == 'estudiante':
        existe_doc = request.user.datosestudiante.grupo_doc.id
        if existe_doc == docente.id:
            estudiantes = {}
            context = {'grupo': grupo, 'estudiantes':estudiantes, 'docente':docente}
            return render(request, 'proyecto/enlace_docente.html', context)
        else:
            return redirect('error_pagina')
    elif grupo == 'tutor':
        objeto_tutor_estu = request.user.datostutor.datosestudiante_set
        existe_doc = objeto_tutor_estu.filter(grupo_doc_id=pk_doc).exists()
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
            return redirect('error_pagina')
    elif grupo == 'administrador':
        context = {'grupo': grupo, 'tutor':tutor}
        return render(request, 'proyecto/enlace_tutor.html', context)
    elif grupo == 'director':
        context = {'grupo': grupo, 'tutor':tutor}
        return render(request, 'proyecto/enlace_tutor.html', context)
    elif grupo == 'estudiante':
        id_tutor = request.user.datosestudiante.tutor.id
        if id_tutor == pk_tutor:
            context = {'grupo': grupo, 'tutor':tutor}
            return render(request, 'proyecto/enlace_tutor.html', context)
        else:
            return redirect('error_pagina')

@login_required(login_url='login')
@admin_only
def registroEstudiante(request):
    grupo = str(request.user.groups.get())
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
            primer_apellido= apellido.split()[0].lower()
            usuario = primer_apellido+'_docente'
            correo = primer_apellido+'_docente@gmail.com'
            password = primer_apellido+'_docente'
            if User.objects.filter(username=usuario).exists():
                messages.info(request, 
            'No se agregó al docente, un docente usa este nombre de usuario')
            elif User.objects.filter(email=correo).exists():
                messages.info(request,
            'No se agregó al docente, un docente usa este mismo correo\
            electrónico')
            elif DatosDocente.objects.filter(grupo=grupo).exists():
                messages.info(request, 
            'No se agregó al docente, otro docente ya se asigno a este grupo')
            elif 2==DatosDocente.objects.filter(mencion=mencion).count():
                messages.info(request, 
            'No se agregó al docente, Solo se admite 2 docentes por mencion')

            else:                 
                # creacion del usuario
                User.objects.create_user(
                        username = usuario,
                        email = correo,
                        first_name = nombre,
                        last_name = apellido,
                        password = password,
                        )
                group = Group.objects.get(name='docente')
                user = User.objects.get(username=usuario)
                user.groups.add(group)
                # creacion de datos
                DatosDocente.objects.create(
                        usuario = User.objects.get(username=usuario),
                        correo = correo,
                        nombre = nombre,
                        apellido = apellido,
                        celular = 'llenar',
                        grupo = grupo,
                        mencion = mencion,
                        )

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
            nombre = form.cleaned_data.get('nombre')
            apellido = form.cleaned_data.get('apellido')
            usuario = correo.split('@')[0] + "_tutor"
            password = usuario
            if User.objects.filter(email=correo).exists():
                messages.info(request,
            'No se agregó al tutor, un usuario usa este mismo correo\
            electrónico')

            else:                 
                # creacion del usuario
                User.objects.create_user(
                        username = usuario,
                        email = correo,
                        first_name = nombre,
                        last_name = apellido,
                        password = password,
                        )
                group = Group.objects.get(name='tutor')
                user = User.objects.get(username=usuario)
                user.groups.add(group)
                # creacion de datos
                DatosTutor.objects.create(
                        usuario = User.objects.get(username=usuario),
                        correo = correo,
                        nombre = nombre,
                        apellido = apellido,
                        celular = 'llenar',
                        )
                messages.success(request, 'Tutor Registrado con exito!!!')
    context = {'form':form}
    return render(request, 'proyecto/agregar_tutor.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso1()
def paso1(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    # link reglamentos
    # links = Reglamento.objects.all()
    # titulos = [link.archivo.name for link in links]
    # dicc_link = {}
    # for n in range(len(links)):
        # dicc_link[links[n]] = titulos[n]
    # progreso = Progreso.objects.get(usuario=estudiante)
    # material estudiante
    # id_usuario_docente = request.user.datosestudiante.grupo_doc.usuario_id
    # usuario_docente = User.objects.get(pk=id_usuario_docente)

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

    context = {'grupo': grupo, 
            # 'links':links, 'titulos':titulos, 
            # 'dicc_link':dicc_link, 'material_docente':material_docente,
            'material_docente':material_docente,
            'estudiante':estudiante,
            'dicc_reglamento':dicc_reglamento,
            'dicc_material':dicc_material,
            # 'progreso': progreso,
            }
    return render(request, 'proyecto/estudiante_paso1.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso1()
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
@permitir_paso1()
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
@permitir_paso2()
def paso2(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    progreso = Progreso.objects.get(usuario=estudiante)
    if request.method == 'POST':
        buscado = request.POST['buscado']
        frase_busqueda = request.POST.get('habilitar')
        tesis_df = pd.read_csv("~/csv_json_files/proyectos_carrera_etn/proy_titulo_autor.csv")
        lista_nombres = [item for item in tesis_df['NOMBRE']]
        lista_titulos = [item for item in tesis_df['TITULO']]
        # agrego de base de datos
        lista_titulos_sistema = [m.titulo for m in BusquedaProyecto.objects.all()]
        lista_nombres_sistema = [m.autor for m in BusquedaProyecto.objects.all()]
        lista_titulos = lista_titulos + lista_titulos_sistema
        lista_nombres = lista_nombres + lista_nombres_sistema
        stop_words = set(stopwords.words('spanish')) 
        # search_terms = 'servicio de voz'
        search_terms = buscado
        vectorizer = TfidfVectorizer(stop_words=stop_words)
        vectors = vectorizer.fit_transform([search_terms] + lista_titulos)
        cosine_similarities = linear_kernel(vectors[0:1], vectors).flatten()
        titulo_scores = [round(item.item()*100,1) for item in cosine_similarities[1:]]  # convert back to native Python dtypes
        score_titles = list(zip(titulo_scores, lista_titulos))
        ordenado_score = sorted(score_titles, reverse=True, key=lambda x:x[0])[:20] 
        dicc_score = {}
        for score_titulo in ordenado_score:
            dicc_score[score_titulo[0]] = score_titulo[1]
        context = {'grupo': grupo,'dicc_score':dicc_score,
                'buscado':buscado,'progreso':progreso}
    else:
        context = {'grupo': grupo,'progreso': progreso}
    return render(request, 'proyecto/estudiante_paso2.html', context)

@login_required(login_url='login')
def busquedaProyectos(request):
    grupo = request.user.groups.get().name
    if request.method == 'POST':
        buscado = request.POST['buscado']
        frase_busqueda = request.POST.get('habilitar')
        tesis_df = pd.read_csv("~/csv_json_files/proyectos_carrera_etn/proy_titulo_autor.csv")
        lista_nombres = [item for item in tesis_df['NOMBRE']]
        lista_titulos = [item for item in tesis_df['TITULO']]
        # agregando a las listas nombres y titulos de la base de datos
        lista_titulos_sistema = [m.titulo for m in BusquedaProyecto.objects.all()]
        lista_nombres_sistema = [m.autor for m in BusquedaProyecto.objects.all()]
        lista_titulos = lista_titulos + lista_titulos_sistema
        lista_nombres = lista_nombres + lista_nombres_sistema
        stop_words = set(stopwords.words('spanish')) 
        # search_terms = 'servicio de voz'
        search_terms = buscado
        vectorizer = TfidfVectorizer(stop_words=stop_words)
        vectors = vectorizer.fit_transform([search_terms] + lista_titulos)
        cosine_similarities = linear_kernel(vectors[0:1], vectors).flatten()
        titulo_scores = [round(item.item()*100,1) for item in cosine_similarities[1:]]  # convert back to native Python dtypes
        score_titles = list(zip(titulo_scores, lista_titulos, lista_nombres))
        ordenado_score = sorted(score_titles, reverse=True, key=lambda x:
                x[0])[:20] 
        dicc_score = {}
        for score_titulo in ordenado_score:
            dicc_score[score_titulo[0]] = score_titulo[1]
        context = {'grupo': grupo,'dicc_score':dicc_score,
                'buscado':buscado}
    else:
        context = {'grupo': grupo,}
    return render(request, 'proyecto/busqueda.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador'])
def agregarProyecto(request):
    grupo = request.user.groups.get().name
    form = BusquedaProyectoForm
    if request.method == 'POST':
        form = BusquedaProyectoForm(request.POST)
        if form.is_valid():
            # file = form.save(commit=False)
            form.save()
            return redirect('busqueda')
    context = {'grupo': grupo,'form':form}
    return render(request, 'proyecto/agregar_proyecto.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso3()
def paso3(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    tutor = estudiante.tutor
    # registro de tutor
    if request.method == 'POST':
        correo = request.POST['agregar_tutor']
        # si el tutor ya fue registrado
        if DatosTutor.objects.filter(correo=correo).exists():
            user_est = request.user.datosestudiante
            user_est.tutor = DatosTutor.objects.get(correo=correo)
            user_est.save()
            # creacion de salas tutor-estudiante
            id_tutor = str(DatosTutor.objects.get(correo=correo).usuario_id)
            id_estudiante = str(request.user.id)
            nombre_sala = id_tutor + id_estudiante
            Sala.objects.create(nombre_sala = nombre_sala)
        else: 
            usuario = correo.split('@')[0]
            # creacion de usuario tutor
            User.objects.create_user(
                    username = usuario + '_tutor',
                    email = correo,
                    first_name = usuario + '_sin_llenar',
                    last_name = 'sin_llenar',
                    password = usuario + '_tutor',
                    )
            # agregando a grupo tutor
            group = Group.objects.get(name='tutor')
            user = User.objects.get(email=correo)
            user.groups.add(group)
            # creacion de datos tutor
            dato_tutor = DatosTutor()
            dato_tutor.usuario = User.objects.get(email=correo)
            dato_tutor.correo = correo
            dato_tutor.nombre = usuario + '_nombre'
            dato_tutor.apellido= 'sin_llenar'
            dato_tutor.celular= 'sin_llenar'
            dato_tutor.save()
            # relacionando estudiante al tutor
            user_est = request.user.datosestudiante
            user_est.tutor = DatosTutor.objects.get(correo=correo)
            user_est.save()
            # creacion de salas tutor-estudiante
            id_tutor = str(DatosTutor.objects.get(correo=correo).usuario_id)
            id_estudiante = str(request.user.id)
            nombre_sala = id_tutor + id_estudiante
            Sala.objects.create(nombre_sala = nombre_sala)
        # progreso = Progreso.objects.get(usuario=estudiante)
        # progreso.nivel = 35
        # progreso.save()
        return redirect('paso3')
    mensaje = 'Ya se le asigno el tutor'
    context = {'grupo': grupo, 'tutor':tutor, 'estudiante':estudiante}
    return render(request, 'proyecto/estudiante_paso3.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
# @permitir_paso3()
def reporteTutorAcepto(request, id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    reporte_tutor_acepto(buffer, estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte_aceptacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor',])
# @permitir_paso3()
def reporteIndicacionesTutor(request, id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    http_host = request.META.get('HTTP_HOST')
    docReporteIndicacionTutor(buffer, estudiante, http_host)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte_aceptacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso4()
def paso4(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    registro_perfil_existe = RegistroPerfil.objects.filter(usuario=estudiante).exists()
    progreso = Progreso.objects.get(usuario=estudiante)
    perfil = RegistroPerfil.objects.filter(usuario=estudiante)
    context = {'grupo': grupo,'registro_perfil_existe': registro_perfil_existe,
            'progreso': progreso,'perfil':perfil,'estudiante':estudiante}
    return render(request, 'proyecto/estudiante_paso4.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso4()
def entregaPerfil(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    estudiante = usuario.datosestudiante
    docente = estudiante.grupo_doc
    tutor = estudiante.tutor
    salas = SalaRevisar.objects.filter(estudiante_rev=estudiante) 
    dicc_sala = {}
    for sala in salas:
        mensajes_doc = MensajeDocenteRevisar.objects.filter(sala=sala)
        mensajes_tut = MensajeTutorRevisar.objects.filter(sala=sala)
        no_visto_docente = 0
        for mensaje_doc in mensajes_doc:
            if not mensaje_doc.visto_estudiante:
                no_visto_docente += 1
        no_visto_tutor = 0
        for mensaje_tut in mensajes_tut:
            if not mensaje_tut.visto_estudiante:
                no_visto_tutor += 1
        dicc_sala[sala] = [no_visto_docente, no_visto_tutor]
    context = {'grupo': grupo,
            'salas':salas,
            'dicc_sala':dicc_sala,
            # 'no_visto_docente':no_visto_docente,
            'estudiante':estudiante}
    return render(request, 'proyecto/entrega_perfil.html', context)

@permitir_paso4()
@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def crearSalaRevisar(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    estudiante = usuario.datosestudiante
    docente = estudiante.grupo_doc
    tutor = estudiante.tutor
    if request.method == 'POST':
        form = SalaRevisarForm(request.POST, request.FILES)
        if form.is_valid():
            nombre_sala = request.POST['sala']
            file = form.save(commit=False)
            file.docente_rev = docente
            file.tutor_rev= tutor
            file.estudiante_rev = estudiante
            file.sala = nombre_sala
            file.save()
            return redirect('entrega_perfil')
            # messages.success(request, 'Se creó la sala revisión con éxito!!!')
    else: 
        form = SalaRevisarForm
    context = {'grupo': grupo,'form':form,}
    return render(request, 'proyecto/crear_sala_revisar.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','docente','tutor'])
def salaRevisar(request, pk_sala):
    grupo = request.user.groups.get().name
    usuario = request.user
    info_estu = SalaRevisar.objects.get(id=pk_sala)
    if grupo == 'docente':
        if request.method == "POST":
            form= MensajeDocenteRevisarForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.visto_docente = True
                file.save()
        else:
            form= MensajeDocenteRevisarForm
        mensajes_doc = MensajeDocenteRevisar.objects.filter(sala=info_estu).order_by('-fecha_creacion')
        for mensaje_doc in mensajes_doc:
            mensaje_doc.visto_docente= True
            mensaje_doc.save()
        mensajes_tut={}
    elif grupo == 'tutor':
        if request.method == "POST":
            form= MensajeTutorRevisarForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.visto_tutor = True
                file.save()
        else:
            form= MensajeTutorRevisarForm()
        mensajes_tut= MensajeTutorRevisar.objects.filter(sala=info_estu).order_by('-fecha_creacion')
        for mensaje_tut in mensajes_tut:
            mensaje_tut.visto_tutor = True
            mensaje_tut.save()
        mensajes_doc={}
    context = {'grupo': grupo, 'info_estu':info_estu,
            'form':form,
            'mensajes_doc':mensajes_doc,
            'mensajes_tut':mensajes_tut,
    }
    return render(request, 'proyecto/sala_revisar.html', context)

@permitir_paso4()
@login_required(login_url='login')
def salaRevisarEstDoc(request, pk_sala):
    grupo = request.user.groups.get().name
    usuario = request.user
    sala = SalaRevisar.objects.get(id=pk_sala)
    if grupo == 'estudiante':
        if request.method == "POST":
            form= MensajeDocenteRevisarForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = sala
                file.usuario = usuario
                file.visto_estudiante = True
                file.save()
        else:
            form = MensajeDocenteRevisarForm
    mensajes_doc = MensajeDocenteRevisar.objects.filter(sala=sala).order_by('-fecha_creacion')
    mensajes_tut= MensajeTutorRevisar.objects.filter(sala=sala).order_by('-fecha_creacion')
    for mensaje_doc in mensajes_doc:
        mensaje_doc.visto_estudiante = True
        mensaje_doc.save()
    context = {'grupo': grupo, 'info_estu':sala,
            'form':form,
            'mensajes_doc':mensajes_doc,
            'mensajes_tut':mensajes_tut,
            }
    return render(request, 'proyecto/sala_revisar_est_doc.html', context)

@permitir_paso4()
@login_required(login_url='login')
def salaRevisarEstTut(request, pk_sala):
    grupo = request.user.groups.get().name
    usuario = request.user
    info_estu = SalaRevisar.objects.get(id=pk_sala)
    if grupo == 'estudiante':
        if request.method == "POST":
            form= MensajeTutorRevisarForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.save()
        else:
            form = MensajeTutorRevisarForm
    mensajes_doc = MensajeDocenteRevisar.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    mensajes_tut= MensajeTutorRevisar.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    for mensaje_tut in mensajes_tut:
        mensaje_tut.visto_estudiante = True
        mensaje_tut.save()
    context = {'grupo': grupo, 'info_estu':info_estu,
            'form':form,
            'mensajes_doc':mensajes_doc,
            'mensajes_tut':mensajes_tut,
            }
    return render(request, 'proyecto/sala_revisar_est_tut.html', context)

@permitir_paso4()
@login_required(login_url='login')
def carta_aceptacion_tutor(request):
    buffer = io.BytesIO()
    estudiante = request.user.datosestudiante
    carta_aceptacion(buffer, estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_aceptacion.pdf')

@permitir_paso4()
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
@permitir_paso4()
def registro_perfil(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    if request.method == "POST":
        form= RegistroPerfilForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.usuario = estudiante
            file.save()
            return render(request, 'proyecto/exito_registro_perfil.html')
    else:
        form = RegistroPerfilForm()
    context = {'grupo': grupo, 'form':form,}
    return render(request, 'proyecto/registro_perfil.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso4()
def ver_perfil_registrado(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    perfil = RegistroPerfil.objects.get(usuario=estudiante)
    context = {'grupo': grupo,'perfil':perfil}
    return render(request, 'proyecto/ver_perfil_registrado.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso4()
def cronograma_actividad(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    cronograma = ActividadesCronograma.objects.filter(usuario=estudiante)
    existe_cronograma = RegistroCronograma.objects.filter(usuario=estudiante).exists()
    if existe_cronograma:
        registro_cronograma = RegistroCronograma.objects.get(usuario=estudiante)
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
            file.usuario = estudiante
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
@allowed_users(allowed_roles=['docente','tutor','director'])
# @permitir_paso4()
def ver_cronograma(request, id_est):
    grupo = request.user.groups.get().name
    if grupo == 'tutor':
        estudiante = request.user.datostutor.datosestudiante_set.get(id=id_est)
    elif grupo == 'director':
        estudiante = DatosEstudiante.objects.get(id=id_est)
    elif grupo == 'docente':
        estudiante = request.user.datosdocente.datosestudiante_set.get(id=id_est)
    cronograma = ActividadesCronograma.objects.filter(usuario=estudiante)
    existe_cronograma = RegistroCronograma.objects.filter(usuario=estudiante).exists()
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
    registro_cronograma = RegistroCronograma.objects.get(usuario=estudiante)
    context = {'grupo': grupo,'cronograma':cronograma, 
            'max_semana': max_semana,
            'estudiante': estudiante,
            'dicc_crono': dicc_crono,
            'registro_cronograma': registro_cronograma,
            'existe_cronograma': existe_cronograma}
    return render(request, 'proyecto/cronograma_actividad.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso4()
def cronograma_registrar(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    if request.method == "POST":
        form= RegistroCronogramaForm(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.usuario = estudiante
            file.save()
            return redirect('cronograma_actividad')
    form= RegistroCronogramaForm()
    context = {'grupo': grupo,'form':form} 
    return render(request, 'proyecto/cronograma_registrar.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso4()
def eliminar_actividad(request, id_act):
    ActividadesCronograma.objects.get(id=id_act).delete()
    return redirect('cronograma_actividad')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
# @permitir_paso4()
def formulario_1(request,id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    # cargo = 'director'
    # lugar = 'instituto de electrónica aplicada'
    # institucion = 'facultad de ingeniería'
    # info_estu = [
            # estudiante.__str__(),
            # estudiante.carnet,
            # estudiante.extension,
            # estudiante.tutor.__str__(),
            # estudiante.grupo_doc.__str__(),
            # estudiante.registroperfil.titulo,
            # estudiante.mencion,
            # ]
    formulario1(buffer,estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_1.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso5()
def paso5(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    proyecto_grado = ProyectoDeGrado.objects.filter(usuario=estudiante).exists()
    proyecto = ProyectoDeGrado.objects.filter(usuario=estudiante)
    progreso = Progreso.objects.get(usuario=estudiante)
    context = {'grupo': grupo, 'progreso': progreso,'proyecto_grado':proyecto_grado,
            'proyecto':proyecto,'estudiante':estudiante}
    return render(request, 'proyecto/estudiante_paso5.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso5()
def cronograma_control(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    cronograma = ActividadesCronograma.objects.filter(usuario=estudiante)
    # fecha de registro del cronograma o fecha de registro del proyecto
    fecha = RegistroPerfil.objects.get(usuario=estudiante).fecha_creacion
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
@permitir_paso5()
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
@permitir_paso5()
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
@permitir_paso5()
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
@permitir_paso5()
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
@permitir_paso6()
def paso6(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    progreso = Progreso.objects.get(usuario=estudiante)
    context = {'grupo': grupo, 
            'progreso': progreso,
            'estudiante': estudiante }
    return render(request, 'proyecto/estudiante_paso6.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso5()
def registroProyecto(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    if request.method == 'POST':
        form = ProyectoDeGradoForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.usuario = estudiante
            file.save()
        return redirect('paso5')
    else: 
        form = ProyectoDeGradoForm
    context = {'grupo': grupo,'form':form,}
    return render(request, 'proyecto/registro_proyecto.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso5()
def ver_proyecto_grado(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    proyecto = ProyectoDeGrado.objects.get(usuario=estudiante)
    context = {'grupo': grupo,'proyecto':proyecto}
    return render(request, 'proyecto/ver_proyecto_grado.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
# @permitir_paso6()
def carta_final_tutor(request, id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    carta_final(buffer, estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_final.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente'])
# @permitir_paso6()
def calificarProyecto(request, id_est):
    grupo = request.user.groups.get().name
    usuario = request.user.datosdocente
    estudiante = DatosEstudiante.objects.get(id=id_est)
    if request.method == 'POST':
        form = CalificarProyectoForm(request.POST)
        nota1 = request.POST['nota1']
        nota2 = request.POST['nota2']
        nota3 = request.POST['nota3']
        nota4 = request.POST['nota4']
        proyecto = ProyectoDeGrado.objects.get(usuario=estudiante)
        proyecto.nota_tiempo_elaboracion = nota1
        proyecto.nota_expos_seminarios = nota2
        proyecto.nota_informes_trabajo = nota3
        proyecto.nota_cumplimiento_cronograma = nota4
        proyecto.calificacion = int(nota1)+int(nota2)+int(nota3)+int(nota4)
        proyecto.save()
        return redirect('progreso_estudiante',pk_est=id_est)
    else: 
        form = CalificarProyectoForm
    context = {'grupo': grupo,'estudiante':estudiante, 'form': form}
    return render(request, 'proyecto/calificar_proyecto.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso6()
def ultimosFormularios(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    context = {'grupo': grupo,'estudiante':estudiante}
    return render(request, 'proyecto/ultimos_formularios.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor'])
# @permitir_paso6()
def materialParaEst(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    if request.method == 'POST':
        form = MaterialDocenteForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.propietario = usuario
            file.save()
    else: 
        form = MaterialDocenteForm
    material = MaterialDocente.objects.filter(propietario=request.user)
    context = {'grupo': grupo,'form':form, 'material':material}
    return render(request, 'proyecto/material_para_estudiante.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
# @permitir_paso6()
def formulario_2(request, id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    proyecto = ProyectoDeGrado.objects.get(usuario=estudiante)
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    info_estu = [
            estudiante.__str__(),
            estudiante.tutor.__str__(),
            estudiante.grupo_doc.__str__(),
            proyecto.titulo,
            estudiante.mencion,
            proyecto.resumen,
            proyecto.fecha_creacion,
            ]
    formulario2(buffer,estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_2.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
# @permitir_paso6()
def formulario_3(request, id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    proyecto = ProyectoDeGrado.objects.get(usuario=estudiante)
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    formulario3(buffer,estudiante,proyecto)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_3.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente'])
# @permitir_paso6()
def auspicioF3(request, id_est):
    grupo = request.user.groups.get().name
    estudiante = DatosEstudiante.objects.get(id=id_est)
    if not Auspicio.objects.filter(usuario=estudiante).exists():
        Auspicio.objects.create(usuario=estudiante)
    auspicio_est = Auspicio.objects.get(usuario=estudiante)
    form = AuspicioForm(instance=auspicio_est)
    if request.method == 'POST':
        form = AuspicioForm(request.POST, instance=auspicio_est)
        if form.is_valid():
            # file = form.save(commit=false)
            # file.usuario = estudiante
            # file.save()
            form.save()
            return redirect('ultimos_formularios')
    context = {'grupo': grupo,'form':form,'estudiante':estudiante}
    return render(request, 'proyecto/auspicio_f3.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
# @permitir_paso6()
def formulario_4(request, id_est):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=id_est)
    proyecto = ProyectoDeGrado.objects.get(usuario=estudiante)
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    extension = 'L.P.'
    cargo = 'director'
    lugar = 'instituto de electrónica aplicada'
    institucion = 'facultad de ingeniería'
    formulario4(buffer,estudiante, proyecto)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_4.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso1()
def confirmarPaso1(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    progreso = Progreso.objects.get(usuario=estudiante)
    if request.method == 'POST':
        confirmar = request.POST['confirmar']
        confirmar = int(confirmar)
        if 1 <= confirmar < 14:
            progreso.nivel = 14
        if 14 <= confirmar < 21:
            progreso.nivel = 21
        if 35 <= confirmar < 64:
            progreso.nivel = 64
        # if confirmar < 19 and confirmar >= 1:
            # progreso.nivel = 19
        # elif confirmar < 25 and confirmar >= 19:
            # progreso.nivel = 25
        # elif confirmar < 25 and confirmar >= 19:
            # progreso.nivel = 25
        # elif confirmar < 69 and confirmar >= 25:
            # progreso.nivel = 69
        progreso.save()
        return redirect('estudiante')
    context = {'grupo': grupo, 'progreso': progreso}
    return render(request, 'proyecto/confirmar_paso.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso5()
def confirmarPaso5(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    progreso = Progreso.objects.get(usuario=estudiante)
    if request.method == 'POST':
        confirmar = request.POST['confirmar']
        confirmar = int(confirmar)
        # if confirmar < 81 and confirmar >= 69:
        if 64 <= confirmar < 86:
            progreso.nivel = 86
        progreso.save()
        return redirect('estudiante')
    context = {'grupo': grupo, 'progreso': progreso}
    return render(request, 'proyecto/confirmar_paso.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso6()
def confirmarPaso6(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    progreso = Progreso.objects.get(usuario=estudiante)
    if request.method == 'POST':
        confirmar = request.POST['confirmar']
        confirmar = int(confirmar)
        # if confirmar < 100 and confirmar >= 81:
        if 86 <= confirmar < 100:
            progreso.nivel = 100
            # agregando a lista de titulados
            DatosEstudianteTitulado.objects.create(
                    correo = estudiante.correo,
                    nombre = estudiante.nombre,
                    apellido = estudiante.apellido,
                    carnet = estudiante.carnet,
                    extension = estudiante.extension,
                    registro_uni = estudiante.registro_uni,
                    celular = estudiante.celular, 
                    mencion = estudiante.mencion,
                    tutor = estudiante.tutor,
                    docente = estudiante.grupo_doc,
                    imagen_perfil =estudiante.imagen_perfil,
                    )
        progreso.save()
        return redirect('estudiante')
    context = {'grupo': grupo, 'progreso': progreso}
    return render(request, 'proyecto/confirmar_paso.html', context)

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

def error(request):
    return render(request, 'proyecto/error_pagina.html')

