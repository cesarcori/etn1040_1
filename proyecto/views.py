from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import *
from .models import *
from .cartas import *

from random import randint
# busqueda
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
# import nltk
# from nltk.corpus import stopwords

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
            sin_tutor = User.objects.get(username='sin_tutor')
            DatosEstudiante.objects.create(
                    usuario = User.objects.get(username=info_usuario.usuario),
                    correo = info_usuario.correo,
                    nombre = info_usuario.nombre,
                    apellido = info_usuario.apellido,
                    carnet = info_usuario.carnet,
                    registro_uni = info_usuario.registro_uni,
                    celular = info_usuario.celular,
                    mencion = info_usuario.mencion,
                    grupo_doc = docente_asignado,
                    tutor = DatosTutor.objects.get(nombre='sin_tutor')
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
    estudiante = request.user.datosestudiante
    context = {'grupo': grupo,'progreso':progreso, 'estudiante':estudiante}
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
@allowed_users(allowed_roles=['docente','tutor','administrador'])
def progresoEstudiante(request, pk_est):
    grupo = str(request.user.groups.get())
    progreso = str(50)
    estudiante = DatosEstudiante.objects.get(id=pk_est)
    if grupo == 'docente':
        # evita que se un docente consulte otros estudiantes
        existe_est = request.user.datosdocente.datosestudiante_set.filter(id=pk_est).exists()
        if existe_est:
            info_estu = SalaRevisar.objects.get(estudiante_rev=estudiante)
            salas = SalaRevisar.objects.filter(estudiante_rev=estudiante) 
            context = {'grupo': grupo,'estudiante':estudiante,
                    'progreso':progreso,'info_estu':info_estu,
                    'salas':salas}
            return render(request, 'proyecto/progreso_estudiante.html', context)
        else:
            return redirect('error_pagina')
    elif grupo== 'tutor':
        existe_est = request.user.datostutor.datosestudiante_set.filter(id=pk_est).exists()
        if existe_est:
            info_estu = SalaRevisar.objects.get(estudiante_rev=estudiante)
            salas = SalaRevisar.objects.filter(estudiante_rev=estudiante) 
            context = {'grupo': grupo,'estudiante':estudiante,
                    'progreso':progreso,'info_estu':info_estu,
                    'salas':salas}
            return render(request, 'proyecto/progreso_estudiante.html', context)
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

@login_required(login_url='login')
@admin_only
def listaTutores(request):
    tutores= DatosTutor.objects.all().order_by('apellido')
    context = {'tutores':tutores}
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
@allowed_users(allowed_roles=['estudiante'])
def paso1(request):
    grupo = request.user.groups.get().name
    # link reglamentos
    links = Reglamento.objects.all()
    # titulos = [' '.join(link.archivo.name.split('/')[1].split('.')[0].split('_')).title() for link in links]
    titulos = [link.archivo.name for link in links]
    dicc_link = {}
    for n in range(len(links)):
        dicc_link[links[n]] = titulos[n]
    id_usuario_docente = request.user.datosestudiante.grupo_doc.usuario_id
    usuario_docente = User.objects.get(pk=id_usuario_docente)
    material_docente = MaterialDocente.objects.filter(propietario=usuario_docente)
    context = {'grupo': grupo, 'links':links, 'titulos':titulos, 
            'dicc_link':dicc_link, 'material_docente':material_docente}
    return render(request, 'proyecto/estudiante_paso1.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def paso2(request):
    grupo = request.user.groups.get().name
    context = {'grupo': grupo}
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
        stop_words = set(stopwords.words('spanish')) 
        # search_terms = 'servicio de voz'
        search_terms = buscado
        vectorizer = TfidfVectorizer(stop_words=stop_words)
        vectors = vectorizer.fit_transform([search_terms] + lista_titulos)
        cosine_similarities = linear_kernel(vectors[0:1], vectors).flatten()
        titulo_scores = [item.item() for item in cosine_similarities[1:]]  # convert back to native Python dtypes
        score_titles = list(zip(titulo_scores, lista_titulos))
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
@allowed_users(allowed_roles=['estudiante'])
def paso3(request):
    grupo = request.user.groups.get().name
    tutor = request.user.datosestudiante.tutor
    # registro de tutor
    if request.method == 'POST':
        correo = request.POST['agregar_tutor']
        # si el tutor ya fue registrado
        if DatosTutor.objects.filter(correo=correo).exists():
            user_est = request.user.datosestudiante
            user_est.tutor = DatosTutor.objects.get(correo=correo)
            user_est.save()
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
            id_tutor = str(DatosTutor.objects.last().usuario_id)
            id_estudiante = str(request.user.id)
            nombre_sala = id_tutor + id_estudiante
            Sala.objects.create(nombre_sala = nombre_sala)
    mensaje = 'Ya se le asigno el tutor'
    context = {'grupo': grupo, 'tutor':tutor}
    return render(request, 'proyecto/estudiante_paso3.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def paso4(request):
    grupo = request.user.groups.get().name
    context = {'grupo': grupo}
    return render(request, 'proyecto/estudiante_paso4.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def entregaPerfil(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    estudiante = usuario.datosestudiante
    docente = estudiante.grupo_doc
    tutor = estudiante.tutor
    if request.method == 'POST':
        form = MaterialEstudianteForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.propietario = usuario
            file.save()
    else: 
        form = MaterialEstudianteForm
    # material = MaterialEstudiante.objects.filter(estudiante_rev=usuario.datosestudiante)
        salas = SalaRevisar.objects.filter(estudiante_rev=estudiante) 
    context = {'grupo': grupo,'form':form,'salas':salas}
    return render(request, 'proyecto/entrega_perfil.html', context)

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
            messages.success(request, 'Se creó la sala revisión con éxito!!!')
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
                file.save()
        else:
            form= MensajeDocenteRevisarForm
    elif grupo == 'tutor':
        if request.method == "POST":
            form= MensajeTutorRevisarForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.save()
        else:
            form= MensajeTutorRevisarForm()
    mensajes_doc = MensajeDocenteRevisar.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    mensajes_tut = MensajeTutorRevisar.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    context = {'grupo': grupo, 'info_estu':info_estu,
            'form':form,
            'mensajes_doc':mensajes_doc,
            'mensajes_tut':mensajes_tut,
    }
    return render(request, 'proyecto/sala_revisar.html', context)

@login_required(login_url='login')
def salaRevisarEstDoc(request, pk_sala):
    grupo = request.user.groups.get().name
    usuario = request.user
    info_estu = SalaRevisar.objects.get(id=pk_sala)
    if grupo == 'estudiante':
        if request.method == "POST":
            form= MensajeDocenteRevisarForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.sala = info_estu
                file.usuario = usuario
                file.save()
        else:
            form = MensajeDocenteRevisarForm
    mensajes_doc = MensajeDocenteRevisar.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    mensajes_tut= MensajeTutorRevisar.objects.filter(sala=info_estu).order_by('-fecha_creacion')
    context = {'grupo': grupo, 'info_estu':info_estu,
            'form':form,
            'mensajes_doc':mensajes_doc,
            'mensajes_tut':mensajes_tut,
            }
    return render(request, 'proyecto/sala_revisar_est_doc.html', context)

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
    context = {'grupo': grupo, 'info_estu':info_estu,
            'form':form,
            'mensajes_doc':mensajes_doc,
            'mensajes_tut':mensajes_tut,
            }
    return render(request, 'proyecto/sala_revisar_est_tut.html', context)

@login_required(login_url='login')
def carta_aceptacion_tutor(request):
    buffer = io.BytesIO()
    estudiante = request.user.datosestudiante
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    extension = 'L.P.'
    titulo_perfil = 'Diseño e implementación de un sistema de información para el seguimiento y administración de proyectos de grado para la materia ETN-1040. '
    info_estu = [
            estudiante.__str__(),
            estudiante.carnet,
            extension,
            estudiante.tutor.celular,
            estudiante.tutor.correo,
            estudiante.grupo_doc.__str__(),
            estudiante.tutor.__str__(),
            titulo_perfil
            ]
    carta_aceptacion(buffer, info_estu)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_aceptacion.pdf')

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
            extension,
            estudiante.celular,
            estudiante.correo,
            estudiante.grupo_doc.__str__(),
            estudiante.tutor.__str__(),
            cargo, lugar, institucion, 
            ]
    carta_solicitud(buffer, info_estu)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_solicitud.pdf')

@login_required(login_url='login')
def registro_perfil(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    if request.method == "POST":
        form= RegistroPerfilForm(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.sala = info_estu
            file.usuario = usuario
            file.save()
    else:
        form = RegistroPerfilForm()
    context = {'grupo': grupo, 
            'form':form,
    }
    return render(request, 'proyecto/registro_perfil.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def paso5(request):
    grupo = request.user.groups.get().name
    context = {'grupo': grupo}
    return render(request, 'proyecto/estudiante_paso5.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def paso6(request):
    grupo = request.user.groups.get().name
    context = {'grupo': grupo}
    return render(request, 'proyecto/estudiante_paso6.html', context)
# def handle_uploaded_file(f):  
    # with open('material_docente/'+f.name, 'wb+') as destination:  
        # for chunk in f.chunks():
            # destination.write(chunk)  
@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','tutor'])
def materialParaEst(request):
    grupo = request.user.groups.get().name
    usuario = request.user
    if request.method == 'POST':
        # form = MaterialDocenteForm(request.POST, request.FILES,
                # instance=propietario)
        form = MaterialDocenteForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.propietario = usuario
            file.save()
            # form.save()
            # return redirect('material_para_estudiante')
    else: 
        form = MaterialDocenteForm
    material = MaterialDocente.objects.filter(propietario=request.user)
    context = {'grupo': grupo,'form':form, 'material':material}
    return render(request, 'proyecto/material_para_estudiante.html', context)

def error(request):
    return render(request, 'proyecto/error_pagina.html')

