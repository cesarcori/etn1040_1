from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from proyecto.decorators import *

from .funciones import *
from .forms import *

@login_required(login_url='login')
def buscarProyectos(request):
    grupo = request.user.groups.get().name
    if request.method == 'POST':
        buscado = request.POST['buscado']
        dicc_score = searchShowAll(buscado)
        context = {'grupo': grupo,'dicc_score':dicc_score,
                'buscado':buscado}
    else:
        context = {'grupo': grupo,}
    return render(request, 'busquedas/buscar.html', context)

@login_required(login_url='login')
def buscarPorDatos(request):
    grupo = request.user.groups.get().name
    if request.method == 'POST':
        buscado = request.POST['buscado']
        query = searchByData(buscado)
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
            return redirect('busqueda')
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
