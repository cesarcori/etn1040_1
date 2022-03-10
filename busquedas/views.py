from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from proyecto.decorators import *
from itertools import chain

from .funciones import *
from .forms import *

@login_required(login_url='login')
def buscarProyectos(request):
    grupo = request.user.groups.get().name
    if request.method == 'POST':
        buscado = request.POST['buscado']
        score_objeto = searchGeneralDb(buscado)
        # contenido = request.POST.getlist('contenido')
        # print(contenido)
        context = {'grupo': grupo,'score_objeto':score_objeto,
                'buscado':buscado}
    else:
        context = {'grupo': grupo,}
    return render(request, 'busquedas/buscar.html', context)

@login_required(login_url='login')
def buscarPorDatos(request):
    grupo = request.user.groups.get().name
    if request.method == 'POST':
        buscado = request.POST['buscado']
        query_db = searchByData(buscado)
        query_excel = searchByDataExcel(buscado)
        query = list(chain(query_db, query_excel))
        context = {'grupo': grupo,'query':query,
                'buscado':buscado}
    else:
        context = {'grupo': grupo,}
    return render(request, 'busquedas/buscar_datos.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['administrador'])
def agregarProyecto(request):
    grupo = request.user.groups.get().name
    form = ProyectosInscritosForm
    if request.method == 'POST':
        form = ProyectosInscritosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('busquedas:buscar_proyectos')
    context = {'grupo': grupo,'form':form}
    return render(request, 'busquedas/agregar_proyecto.html', context)

@login_required(login_url='login')
def verProyectos(request):
    grupo = request.user.groups.get().name
    proyectos = searchProyectosInscritosCsv()
    context = {'grupo': grupo,'proyectos':proyectos}
    return render(request, 'busquedas/ver_proyectos.html', context)

@login_required(login_url='login')
def buscarDatosProyectosExcel(request):
    grupo = request.user.groups.get().name
    if request.method == 'POST':
        buscado = request.POST['buscado']
        query = searchByDataExcel(buscado)
        context = {'grupo': grupo,'query':query,
                'buscado':buscado}
    else:
        context = {'grupo': grupo,}
    return render(request, 'busquedas/buscar_general.html', context)

@login_required(login_url='login')
def detalleProyecto(request, titulo):
    grupo = request.user.groups.get().name
    if ProyectosExcel.objects.filter(autor=titulo):
        proyecto = ProyectosExcel.objects.filter(autor=titulo)[0]
    elif ProyectosInscritos.objects.filter(autor=titulo):
        proyecto = ProyectosInscritos.objects.filter(autor=titulo)[0]
    else:
        proyecto = None
    context = {'grupo': grupo, 'proyecto':proyecto}
    return render(request, 'busquedas/detalle_proyecto.html', context)



