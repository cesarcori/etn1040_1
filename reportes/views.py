from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from proyecto.decorators import unauthenticated_user, allowed_users, admin_only
from proyecto.models import DatosEstudiante, Equipo, ProyectoDeGrado

from .formularios import *
from .reportes import *
from .cartas import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director','tribunal'])
def cartaTutorAcepto(request, pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    reporte_tutor_acepto(buffer, estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_tutor_acepto.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor',])
def reporteIndicacionesTutor(request, pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    http_host = request.META.get('HTTP_HOST')
    generarReporteIndicacionTutor(buffer, estudiante, http_host)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reporte_indicacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director','tribunal'])
def formularioAceptacion(request,pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    equipo = estudiante.equipo
    generarformularioAceptacion(buffer, equipo)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_aceptacion.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante',])
def firmaTutorCapitulos(request, pk):
    buffer = io.BytesIO()
    # estudiante = DatosEstudiante.objects.get(id=pk)
    equipo = get_object_or_404(Equipo, id=pk)
    generarFirmaTutorCapitulos(buffer, equipo)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='capitulos.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
def cartaFinal(request, pk):
    buffer = io.BytesIO()
    equipo = Equipo.objects.get(id=pk)
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    generarCartaFinal(buffer, equipo)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_final.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
def formularioSolicitudTribunal(request, pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    equipo = estudiante.equipo
    proyecto = ProyectoDeGrado.objects.get(equipo=estudiante.equipo)
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    extension = 'L.P.'
    cargo = 'director'
    lugar = 'instituto de electrónica aplicada'
    institucion = 'facultad de ingeniería'
    generarFormularioSolicituTribunal(buffer, proyecto)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_material.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
def formularioRegistroSeguimiento(request, pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    proyecto = ProyectoDeGrado.objects.get(equipo=estudiante.equipo)
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    generarRegistroSeguimiento(buffer,proyecto)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_registro_seguimiento.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente'])
def auspicioFormRegSeg(request, id_est):
    grupo = request.user.groups.get().name
    estudiante = DatosEstudiante.objects.get(id=id_est)
    if not Auspicio.objects.filter(usuario=estudiante).exists():
        Auspicio.objects.create(usuario=estudiante)
    auspicio_est = Auspicio.objects.get(usuario=estudiante)
    form = AuspicioForm(instance=auspicio_est)
    if request.method == 'POST':
        form = AuspicioForm(request.POST, instance=auspicio_est)
        if form.is_valid():
            form.save()
            return redirect('paso6')
    context = {'grupo': grupo,'form':form,'estudiante':estudiante}
    return render(request, 'proyecto/auspicio_f3.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente','director'])
def formularioMateria(request, pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    # lo siguiente hay que hagregar de alguna forma a la base de datos
    # info_estu = [
            # estudiante.__str__(),
            # estudiante.tutor.__str__(),
            # estudiante.grupo_doc.__str__(),
            # proyecto.titulo,
            # estudiante.mencion,
            # proyecto.resumen,
            # proyecto.fecha_creacion,
            # ]
    generarFormularioMateria(buffer,estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_2.pdf')
