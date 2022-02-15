from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from proyecto.decorators import *
from .forms import *
from actividades.models import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso3()
def individual(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    # actividad = Actividad.objects.get(nombre='elegir modalidad')
    # act_est= estudiante.realizaractividad_set.get(actividad=actividad)
    mensaje = f'¿Está seguro de que desea trabajar en la modalidad INDIVIDUAL?'
    link = ['paso3']
    if not estudiante.actividad.filter(nombre="elegir modalidad").exists():
        actividad = Actividad.objects.get(nombre='elegir modalidad')
        if request.method == 'POST':
            estudiante.modalidad = 'individual'
            estudiante.actividad.add(actividad)
            estudiante.save()
            Equipo.objects.create(nombre=estudiante.correo, cantidad=1)
            equipo_est = Equipo.objects.get(nombre=estudiante.correo)
            equipo_est.cantidad = 1
            equipo_est.save()
            estudiante.equipo = equipo_est
            estudiante.save()
            return redirect('paso3')
        context = {'grupo': grupo, 'estudiante':estudiante,
                'mensaje':mensaje,'link':link,
                }
        return render(request, 'modalidad/confirmar.html', context)
    else:
        return HttpResponse("error")

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
@permitir_paso3()
def multiple(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    # actividad = Actividad.objects.get(nombre='eleccion de modalidad')
    # act_est = estudiante.realizaractividad_set.get(actividad=actividad)
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
@permitir_paso3()
def solicitud(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    # actividad = Actividad.objects.get(nombre='eleccion de modalidad')
    # act_est = estudiante.realizaractividad_set.get(actividad=actividad)
    if estudiante.actividad.filter(nombre="elegir modalidad").exists():
        return HttpResponse('error')
    if estudiante.equipo == None:
        actividad = Actividad.objects.get(nombre='elegir modalidad')
        mensaje = f"Se enviará al docente Ing. {estudiante.grupo_doc}, la solicitud de modalidad Múltiple"
        link = ['modalidad:multiple']
        form = SolicitudForm
        if request.method == 'POST':
            form = SolicitudForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.estudiante= estudiante
                file.docente= estudiante.grupo_doc
                file.save()
                estudiante.modalidad = 'multiple'
                estudiante.actividad.add(actividad)
                estudiante.save()
            return redirect('paso3')
        context = {'grupo': grupo, 'estudiante':estudiante,
                'mensaje':mensaje,'link':link,'form':form
                }
        return render(request, 'modalidad/formulario.html', context)
    else:
        return HttpResponse("error")

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
        return redirect('error_pagina')
    form = RechazarSolicitudForm
    if request.method == 'POST':
        form = RechazarSolicitudForm(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.estudiante= estudiante
            file.docente= estudiante.grupo_doc
            file.save()
            # reestablecer datos estudiante
            actividad = Actividad.objects.get(nombre='elegir modalidad')
            estudiante.modalidad = None
            estudiante.actividad.remove(actividad)
            estudiante.save()
            return redirect('progreso_estudiante', pk_est=estudiante.id)

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
        return redirect('error_pagina')
    # act_est = estudiante.realizaractividad_set.get(actividad=actividad)
    mensaje = f'¿Está seguro de aprobar al estudiante: {estudiante} la modalidad MÚLTIPLE? Ingresar la cantidad de participantes.'
    link = ['modalidad:ver_solicitud',solicitud.pk]
    if not estudiante.actividad.filter(nombre="elegir modalidad").exists():
        return HttpResponse("error")
    else:
        form = AprobarSolicitudForm
        if request.method == 'POST':
            form = AprobarSolicitudForm(request.POST)
            if form.is_valid():
                file = form.save(commit=False)
                file.nombre = estudiante.correo
                file.save()
                estudiante.equipo = Equipo.objects.get(nombre=estudiante.correo)
                estudiante.save()
                solicitud.aprobar = True
                solicitud.save()
                return redirect('progreso_estudiante', pk_est=estudiante.id)
        context = {'grupo': grupo, 'estudiante':estudiante,
                'mensaje':mensaje, 'link':link, 'form':form,
                }
        return render(request, 'modalidad/formulario.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def agregarIntegrantes(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    solicitud_mandar = estudiante.equipo.cantidad -1 - estudiante.interesado.filter(rechazar=False).count()
    solicitudes = estudiante.interesado.filter(rechazar=False)
    if request.method == 'POST':
        correo = request.POST['agregar_integrante']
        # verificar que el correo pertencece a un estudiante que no tiene aun tutor
        estudiantes_permitidos = DatosEstudiante.objects.filter(tutor=None)
        if solicitud_mandar <= 0:
            messages.error(request, 'Ya tienes se completo el numero de solicitudes.')
        elif not DatosEstudiante.objects.filter(correo=correo).exists():
            messages.error(request, 'El correo ingresado no pertenece a un estudiante registrado en el sistema.')
        elif not estudiantes_permitidos.filter(correo=correo).exists():
            messages.error(request, 'El estudiante ya tiene tutor')
        elif estudiante.correo==correo:
            messages.error(request, 'No puedes enviar la solicitud a ti mismo.')
        elif DatosEstudiante.objects.get(correo=correo).modalidad:
            messages.error(request, 'El estudiante ya tiene una modalidad de trabajo.')
        elif estudiante.interesado.filter(correo_invitado=correo, rechazar=False).exists():
            messages.error(request, 'Ya enviaste solicitud a este estudiante.')
        else: 
            estudiante_invitado = DatosEstudiante.objects.get(correo=correo)
            # enviar solicitud al estudiante
            SolicitudIntegrante.objects.create(
                estudiante_interesado = estudiante,
                estudiante_invitado = estudiante_invitado,
                correo_invitado = correo,
                    )
            messages.success(request, f"Se envió la solicitud a {estudiante_invitado}")
            # mostrar solicitud enviada
            return redirect('modalidad:agregar_integrantes')
    context = {'grupo':grupo, 'estudiante':estudiante,
            'solicitud_mandar':solicitud_mandar, 'solicitudes':solicitudes 
            }
    return render(request, 'modalidad/agregar_integrantes.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def verSolicitudInvitado(request):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    solicitudes = estudiante.invitado.filter(rechazar=False)
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
        return redirect('error_pagina')
    mensaje = f'¿Está seguro rechazar la solicitud del estudiante: {solicitud.estudiante_interesado}, para ser parte de su grupo?'
    link = ['modalidad:ver_solicitudes_invitado']
    if request.method == 'POST':
        solicitud.rechazar = True
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
        return redirect('error_pagina')
    mensaje = f'¿Está seguro de ser parte del grupo del estudiante: {solicitud.estudiante_interesado}? No hay marcha atras luego de aceptar ser parte del equipo.'
    link = ['modalidad:ver_solicitudes_invitado']
    if request.method == 'POST':
        solicitud.aprobar= True
        solicitud.save()
        # asignar al equipo.
        # asignar modalidad multiple
        # asignar elegir modalidad

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
    link = ['modalidad:agregar_integrantes']
    form = EquipoForm(instance=equipo)
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('modalidad:agregar_integrantes')
    context = {'grupo':grupo, 'estudiante':estudiante,
            'mensaje':mensaje,'link':link, 'form':form
            }
    return render(request, 'modalidad/formulario.html', context)
