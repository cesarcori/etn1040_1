from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import *
from .models import *

from random import randint

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
            DatosEstudiante.objects.create(
                    usuario = User.objects.get(username=info_usuario.usuario),
                    correo = info_usuario.correo,
                    nombre = info_usuario.nombre,
                    apellido = info_usuario.apellido,
                    carnet = info_usuario.carnet,
                    registro_uni = info_usuario.registro_uni,
                    celular = info_usuario.celular,
                    mencion = info_usuario.mencion,
                    grupo_doc = docente_asignado
                    )
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
@allowed_users(allowed_roles=['estudiante'])
def estudiante(request):
    grupo = 'estudiante'
    progreso = str(50)
    context = {'grupo': grupo,'progreso':progreso}
    return render(request, 'proyecto/estudiante.html', context)

@login_required(login_url='login')
def perfilUsuarios(request):
    grupo = str(request.user.groups.get())
    # id_usuario = request.user.id
    # # switch-case
    # def perfil_admi():
        # usuario = User.objects.get(id=id_usuario)
        # info = usuario.datosadministrador
        # return info
    # def perfil_estudiante():
        # info = DatosEstudiante.objects.all()
        # return info
    # def perfil_docente():
        # info = DatosDocente.objects.all()
        # return info
    # def perfil_tutor():
        # info = DatosTutor.objects.all()
        # return info
    # def perfil_usuario(grupo):
        # grupo_pertenece = {
                # 'administrador': perfil_admi,
                # 'estudiante': perfil_estudiante,
                # 'docente': perfil_docente,
                # 'tutor': perfil_tutor,
                # }
        # func = grupo_pertenece.get(grupo)
        # return func
    # llamando datos del usuario segun grupo que pertenece
    # info_usuario = perfil_usuario(grupo)
    # print(perfil_usuario(grupo))
    context = {'grupo': grupo}
    return render(request, 'proyecto/perfil.html', context)

@login_required(login_url='login')
def busquedaProyectos(request):
    grupo = str(request.user.groups.get())
    context = {'grupo': grupo}
    return render(request, 'proyecto/busqueda.html', context)

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

@login_required(login_url='login')
# hay que aumentar si o si un valor mas del enlace del estudiante o usuario
# pensar seriamente en elaborar 6 tablas para comunicacion entre usuarios
def mensajePersonal(request):
    grupo = str(request.user.groups.get())
    usuario = request.user
    mensaje_estudiantes = {} 
    context = {'grupo': grupo,'mensaje_estudiantes':mensaje_estudiantes}
    return render(request, 'proyecto/mensaje_personal.html', context)

@login_required(login_url='login')
def crearMensajePersonal(request):
    grupo = str(request.user.groups.get())
    if request.method == "POST":
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.autor= request.user
            mensaje.save()
            return redirect('mensaje_personal')
    else:
        form = MensajeForm()
    context = {'grupo': grupo, 'form':form}
    return render(request, 'proyecto/crear_mensaje_personal.html', context)

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
    grupo = str(request.user.groups.get())
    id_tutor= request.user.datosestudiante.tutor.usuario_id
    tutor = User.objects.get(id=id_tutor)
    comunicados = tutor.comunicado_set.all().order_by('-fecha_creacion')
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
@allowed_users(allowed_roles=['docente','tutor','administrador'])
def enlaceEstudiante(request, pk_est):
    grupo = str(request.user.groups.get())
    estudiante = DatosEstudiante.objects.get(id=pk_est)
    if grupo=='administrador':
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
@allowed_users(allowed_roles=['estudiante','tutor','administrador'])
def enlaceDocente(request, pk_doc):
    grupo = request.user.groups.get().name
    docente = DatosDocente.objects.get(id=pk_doc)
    if grupo == 'administrador':
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
    # estudiantes = docente.datosestudiante_set.all()
    # context = {'grupo': grupo, 'estudiantes':estudiantes, 'docente':docente}
    # return render(request, 'proyecto/enlace_docente.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','administrador','estudiante'])
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
@admin_only
def listaDocentes(request):
    docentes = DatosDocente.objects.all().order_by('grupo')
    context = {'docentes':docentes}
    return render(request, 'proyecto/lista_docente.html', context)

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

def error(request):
    return render(request, 'proyecto/error_pagina.html')
