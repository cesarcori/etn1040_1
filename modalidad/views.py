from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from proyecto.decorators import *
from proyecto.models import Equipo
from mensaje.funciones import isVisto
from .forms import *
from actividades.models import *
from actividades.funciones import *


@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2])
def individual(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    mensaje = f'¿Está seguro de que desea trabajar en la modalidad INDIVIDUAL?'
    link = ['paso3']
    if not estudiante.actividad.filter(nombre="elegir modalidad").exists():
        if request.method == 'POST':
            estudiante.modalidad = 'individual'
            estudiante.is_modalidad_aprobada = True
            estudiante.save()
            agregarActividadEstudiante('elegir modalidad', estudiante)
            return redirect('paso3')
        context = {'grupo': grupo, 'estudiante':estudiante,
                'mensaje':mensaje,'link':link,
                }
        return render(request, 'modalidad/confirmar.html', context)
    else:
        return HttpResponse("error")

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2])
def multiple(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    mensaje = f'¿Está seguro de que desea trabajar en la modalidad MÚLTIPLE?'
    link = ['paso3']
    if not estudiante.actividad.filter(nombre="elegir modalidad").exists():
        actividad = Actividad.objects.get(nombre='elegir modalidad')
        if request.method == 'POST':
            return redirect('modalidad:solicitud')
        context = {'grupo': grupo, 'estudiante':estudiante,
                'mensaje':mensaje,'link':link,
                }
        return render(request, 'modalidad/confirmar.html', context)
    else:
        return HttpResponse("error")

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_con(pasos=[1,2])
def solicitud(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    if estudiante.actividad.filter(nombre="elegir modalidad").exists():
        return HttpResponse('error')
    # if not estudiante.equipo == None:
        # return HttpResponse("error")
    mensaje = f"Se enviará al docente Ing. {estudiante.grupo_doc}, la solicitud de modalidad Múltiple"
    link = ['modalidad:multiple']
    form = SolicitudForm
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            form.instance.estudiante = estudiante
            form.instance.docente = estudiante.grupo_doc
            form.save()
            estudiante.modalidad = 'multiple'
            estudiante.save()
            agregarActividadEstudiante('elegir modalidad', estudiante)

        return redirect('paso3')
    context = {'grupo': grupo, 'estudiante':estudiante,
            'mensaje':mensaje,'link':link,'form':form
            }
    return render(request, 'modalidad/formulario.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','estudiante'])
def verSolicitud(request, id_obj):
    grupo = request.user.groups.get().name
    solicitud = get_object_or_404(Solicitud, id=id_obj)
    estudiante = solicitud.estudiante
    if grupo == 'estudiante':
        user_request = request.user.datosestudiante
        user_id = solicitud.estudiante
    if grupo == 'docente':
        user_request = request.user.datosdocente
        user_id = solicitud.estudiante.grupo_doc
    if not user_request == user_id:
        return redirect('error_pagina')
    context = {'grupo':grupo, 'estudiante':estudiante,'solicitud':solicitud}
    return render(request, 'modalidad/ver_solicitud.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente'])
def rechazarSolicitud(request, id_obj):
    grupo = request.user.groups.get().name
    solicitud = get_object_or_404(Solicitud, id=id_obj)
    docente = request.user.datosdocente
    mensaje = f"Redactar los motivos por los cuales no considera que sea un proyecto de participación múltiple."
    link = ['modalidad:ver_solicitud', solicitud.id]
    estudiante = solicitud.estudiante
    if not solicitud.estudiante.grupo_doc == docente:
        return HttpResponse('error')
    form = RechazarSolicitudForm
    if request.method == 'POST':
        form = RechazarSolicitudForm(request.POST)
        if form.is_valid():
            form.instance.estudiante = estudiante
            form.instance.docente = estudiante.grupo_doc
            form.save()
            # file = form.save(commit=False)
            # file.estudiante= estudiante
            # file.docente= estudiante.grupo_doc
            # file.save()
            # reestablecer datos estudiante
            actividad = Actividad.objects.get(nombre='elegir modalidad')
            estudiante.modalidad = None
            estudiante.actividad.remove(actividad)
            estudiante.save()
            return redirect('progreso_estudiante', pk=estudiante.equipo.id)

    context = {'grupo':grupo, 'solicitud':solicitud, 'link':link, 
            'form':form,'mensaje': mensaje}
    return render(request, 'modalidad/formulario.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def verRechazo(request, id_obj):
    grupo = request.user.groups.get().name
    rechazo = get_object_or_404(RechazarSolicitud, id=id_obj)
    estudiante = request.user.datosestudiante
    docente = rechazo.docente
    if not estudiante.grupo_doc == docente:
        return redirect('error_pagina')
    context = {'grupo':grupo, 'estudiante':estudiante,'rechazo':rechazo}
    return render(request, 'modalidad/ver_rechazo.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente'])
def aprobarSolicitud(request, id_obj):
    grupo = request.user.groups.get().name
    solicitud = get_object_or_404(Solicitud, id=id_obj)
    estudiante = solicitud.estudiante
    docente = request.user.datosdocente
    if not solicitud.estudiante.grupo_doc == docente:
        return HttpResponse("error")
    mensaje = f'¿Está seguro de aprobar al estudiante: {estudiante} la modalidad MÚLTIPLE? Ingresar la cantidad de participantes.'
    link = ['modalidad:ver_solicitud',solicitud.pk]
    if not estudiante.actividad.filter(nombre="elegir modalidad").exists():
        return HttpResponse("error")
    else:
        form = AprobarSolicitudForm(instance=estudiante.equipo)
        if request.method == 'POST':
            form = AprobarSolicitudForm(request.POST, instance=estudiante.equipo)
            if form.is_valid():
                form.save()
                solicitud.aprobar = True
                solicitud.save()
                estudiante.equipo.alias = estudiante.equipo.nombre
                estudiante.equipo.save()
                estudiante.is_modalidad_aprobada = True
                estudiante.save()
                return redirect('progreso_estudiante', pk=estudiante.equipo.id)
        context = {'grupo': grupo, 'estudiante':estudiante,
                'mensaje':mensaje, 'link':link, 'form':form,
                }
        return render(request, 'modalidad/formulario.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def agregarIntegrantes(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    equipo = estudiante.equipo
    solicitud_mandar = equipo.cantidad -1 - equipo.interesado.filter(estado=None).count() - equipo.interesado.filter(estado='aprobar').count()
    solicitudes = equipo.interesado.filter(estado=None)
    if request.method == 'POST':
        correo = request.POST['agregar_integrante']
        if solicitud_mandar <= 0:
            messages.error(request, 'Ya tienes completo el número de solicitudes.')
        elif not DatosEstudiante.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo ingresado no pertenece a un estudiante registrado en el sistema.')
        elif not DatosEstudiante.objects.filter(correo=correo, grupo_doc=estudiante.grupo_doc).exists():
            messages.error(request, 'El estudiante no se encuentra en el mismo paraleo del docente.')
        elif estudiante.correo==correo:
            messages.error(request, 'No puedes enviar la solicitud a ti mismo.')
        elif DatosEstudiante.objects.get(correo=correo).modalidad:
            messages.error(request, 'El estudiante ya tiene una modalidad de trabajo.')
        # elif DatosEstudiante.objects.get(correo=correo).actividad.count()<3:
            # messages.error(request, 'El estudiante no concluyo el paso 2.')
        elif equipo.interesado.filter(correo_invitado=correo, estado=None).exists():
            messages.error(request, 'Ya enviaste solicitud a este estudiante.')
        else: 
            estudiante_invitado = DatosEstudiante.objects.get(correo=correo)
            # enviar solicitud al estudiante
            SolicitudIntegrante.objects.create(
                equipo_interesado = equipo,
                estudiante_invitado = estudiante_invitado,
                correo_invitado = correo,
                    )
            messages.success(request, f"Se envió la solicitud a {estudiante_invitado}")
        return redirect('modalidad:agregar_integrantes')
    context = {'grupo':grupo, 'estudiante':estudiante, 'equipo':equipo,
            'solicitud_mandar':solicitud_mandar, 'solicitudes':solicitudes 
            }
    return render(request, 'modalidad/agregar_integrantes.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def verSolicitudInvitado(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    solicitudes = estudiante.invitado.filter(estado=None)
    if estudiante.modalidad:
        return HttpResponse('error')
    context = {'grupo':grupo, 'estudiante':estudiante,'solicitudes':solicitudes
        }
    return render(request, 'modalidad/ver_solicitud_invitado.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def rechazarSolicitudInvitado(request,pk):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    solicitud = get_object_or_404(SolicitudIntegrante, id=pk)
    if not solicitud.estudiante_invitado == estudiante:
        return HttpResponse('error')
    if estudiante.modalidad == individual:
        return HttpResponse('error')
    mensaje = f'¿Está seguro rechazar la solicitud del estudiante: {solicitud.equipo_interesado}, para ser parte de su grupo?'
    link = ['modalidad:ver_solicitudes_invitado']
    if request.method == 'POST':
        solicitud.estado = 'rechazar'
        solicitud.save()
        return redirect('home')
    context = {'grupo': grupo, 'estudiante':estudiante,
            'mensaje':mensaje, 'link':link, 
            }
    return render(request, 'modalidad/confirmar.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def aprobarSolicitudInvitado(request, pk):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    solicitud = get_object_or_404(SolicitudIntegrante, id=pk)
    if not solicitud.estudiante_invitado == estudiante:
        return HttpResponse('error')
    if estudiante.modalidad:
        return HttpResponse('error')
    mensaje = f'¿Está seguro de ser parte del grupo del estudiante: {solicitud.equipo_interesado}? No hay marcha atras luego de aceptar ser parte del equipo.'
    link = ['modalidad:ver_solicitudes_invitado']
    if request.method == 'POST':
        # actividad = Actividad.objects.get(nombre='elegir modalidad')
        solicitud.estado = 'aprobar'
        solicitud.save()
        # cambiar el nombre del equipo
        solicitud.equipo_interesado.nombre = f"{solicitud.equipo_interesado.nombre} : {estudiante.equipo.nombre}"
        solicitud.equipo_interesado.save()
        # asignar al equipo.
        estudiante.equipo = solicitud.equipo_interesado
        # asignar modalidad multiple
        estudiante.modalidad = 'multiple'
        estudiante.is_modalidad_aprobada = True
        # asignar elegir modalidad
        # estudiante.actividad.add(actividad)
        agregarActividadEstudiante('estudiar reglamentos', estudiante)
        agregarActividadEstudiante('material docente', estudiante)
        agregarActividadEstudiante('busqueda proyecto', estudiante)
        agregarActividadEstudiante('elegir modalidad', estudiante)
        # guardar todos los cambios
        estudiante.save()
        # rechazar a todas las demas solicitudes.
        solicitudes = estudiante.invitado.all().exclude(equipo_interesado=solicitud.equipo_interesado)
        for solicitud in solicitudes:
            solicitud.estado = 'rechazar'
            solicitud.save()
        return redirect('home')

    context = {'grupo': grupo, 'estudiante':estudiante,
            'mensaje':mensaje, 'link':link, 
            }
    return render(request, 'modalidad/confirmar.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def modificarNombreEquipo(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    equipo = estudiante.equipo
    mensaje = f'Cambiar nombre del grupo'
    link = ['modalidad:ver_equipo',equipo.pk]
    form = EquipoForm(instance=equipo)
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('modalidad:ver_equipo', pk=equipo.pk)
    context = {'grupo':grupo, 'estudiante':estudiante,
            'mensaje':mensaje,'link':link, 'form':form
            }
    return render(request, 'modalidad/formulario.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','tribunal','director'])
def verEquipo(request, pk):
    equipo = get_object_or_404(Equipo, id=pk)
    grupo = request.user.groups.get().name
    estudiantes = equipo.datosestudiante_set.all()
    estudiante_isVisto = {}
    if grupo == 'docente' or grupo == 'tutor' or grupo == 'estudiante':
        for estudiante in estudiantes:
            is_visto = isVisto(estudiante.usuario, request.user)
            estudiante_isVisto[estudiante] = is_visto
            # estudiante_isVisto[estudiante] = True
    else:
        for estudiante in estudiantes:
            estudiante_isVisto[estudiante] = False
    context = {'grupo':grupo, 'equipo':equipo, 'estudiante_isVisto': estudiante_isVisto}
    return render(request, 'modalidad/ver_equipo.html', context)
    
