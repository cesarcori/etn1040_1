from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from proyecto.decorators import unauthenticated_user, allowed_users, admin_only
from proyecto.models import DatosEstudiante, Equipo, ProyectoDeGrado

from .formularios import *
from .reportes import *
from .cartas import *
from .form import *
from actividades.funciones import *

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
    generarRegistroSeguimiento(buffer,estudiante,proyecto)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_registro_seguimiento.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor','docente'])
def auspicioFormRegSeg(request, pk):
    grupo = request.user.groups.get().name
    estudiante = DatosEstudiante.objects.get(id=pk)
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
    generarFormularioMateria(buffer,estudiante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='formulario_2.pdf')

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','administrador','docente','tutor','director'])
def reporteEstudianteHtml(request, pk):
    grupo = request.user.groups.get().name
    estudiante = DatosEstudiante.objects.get(id=pk)
    pasos_realizados = len(pasosRealizados(estudiante))
    if pasos_realizados == 0:
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
    if pasos_realizados >= 1:
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
    if pasos_realizados >= 2:
        pasos['Paso 2'] = ['Búsqueda de Proyectos de Grado']
        del pasos_falta['Paso 2']
    if pasos_realizados >= 3:
        pasos['Paso 3'] = ['Asignación de Tutor de Proyecto de Grado',
                        'Carta aceptación de Tutoría']
        del pasos_falta['Paso 3']
    if pasos_realizados >= 4:
        pasos['Paso 4'] = ['Entrega y revisión de Perfil de Proyecto de Grado',
                        'Registro de Perfil de Proyecto de Grado',
                        'Registro de Cronograma de Proyecto de Grado',
                        'Formulario 1']
        del pasos_falta['Paso 4']
    if pasos_realizados >= 5:
        pasos['Paso 5'] = ['Cumplir con el cronograma',
                        'Revisión del Proyecto de Grado',
                        'Registro del Proyecto de Grado',]
        del pasos_falta['Paso 5']
    if pasos_realizados >= 6:
        pasos['Paso 6'] = ['Carta de Conclusión',
                    'Gegeración de los 3 formularios']
        del pasos_falta['Paso 6']
    context = {'grupo':grupo,'estudiante':estudiante, 'pasos':pasos, 'pasos_falta':pasos_falta}
    return render(request, 'reportes/reporte_estudiante.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','administrador','docente','tutor','director'])
def reporteEstudiante(request, pk):
    buffer = io.BytesIO()
    estudiante = DatosEstudiante.objects.get(id=pk)
    usuario_solicitante = request.user
    generarReporteEstudiante(buffer, estudiante, usuario_solicitante)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='carta_aceptacion.pdf')
