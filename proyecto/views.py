from django.shortcuts import render

def bienvenidos(request):
    return render(request, 'proyecto/bienvenidos.html')
def docente(request):
    return render(request, 'proyecto/docente.html')
def tutor(request):
    return render(request, 'proyecto/tutor.html')
def estudiante(request):
    return render(request, 'proyecto/estudiante.html')
def perfilUsuarios(request):
    return render(request, 'proyecto/perfil.html')
def busquedaProyectos(request):
    return render(request, 'proyecto/busqueda.html')

