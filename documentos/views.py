from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse

from proyecto.decorators import *
from .forms import *
from .models import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def verDocumento(request):
    context = {}
    return render(request, 'mensaje/index.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante'])
def subirDocumento(request, tipo):
    grupo = request.user.groups.get().name
    estudiante = request.user.datosestudiante
    equipo = estudiante.equipo
    # documento = Documento.objects.filter(equipo=equipo, tipo=tipo).last()
    documento, created = Documento.objects.get_or_create(equipo=equipo, tipo=tipo)
    form = SubirDocumentoForm(instance=documento)
    if request.method == 'POST':
        form = SubirDocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.instance.equipo = estudiante.equipo
            form.instance.tipo = tipo
            form.save()
        return redirect('documentos:subir_documento', tipo=tipo)
    context = {'grupo': grupo,'form':form, 'documento':documento}
    return render(request, 'documentos/subir_documento.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','estudiante','director','tutor','tribunal'])
def verDocumento(request, pk, tipo):
    grupo = request.user.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)
    documento = get_object_or_404(Documento, equipo=equipo, tipo=tipo)
    filepath = documento.archivo.file.name
    return FileResponse(open(filepath, 'rb'))
