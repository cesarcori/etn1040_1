from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from etn1040_1.settings import MEDIA_ROOT

from proyecto.decorators import *
from .forms import *
from .models import *
from proyecto.models import DatosEstudiante

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor','docente','tribunal','estudiante'])
def verDocumentoIndex(request):
    context = {}
    return render(request, 'mensaje/index.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['estudiante','tutor'])
def subirDocumento(request, tipo, pk):
    grupo = request.user.groups.get().name
    # estudiante = request.user.datosestudiante
    estudiante = get_object_or_404(DatosEstudiante, id=pk)
    equipo = estudiante.equipo
    documento, created = Documento.objects.get_or_create(equipo=equipo, tipo=tipo)
    form = SubirDocumentoForm(instance=documento)
    if request.method == 'POST':
        form = SubirDocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.instance.equipo = estudiante.equipo
            form.instance.tipo = tipo
            form.save()
        return redirect('documentos:subir_documento', tipo=tipo, pk=pk)
    context = {'grupo': grupo,'form':form, 'documento':documento}
    return render(request, 'documentos/subir_documento.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['docente','estudiante','director','tutor','tribunal'])
def verDocumento(request, pk, tipo):
    grupo = request.user.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)
    if Documento.objects.filter(equipo=equipo, tipo=tipo).exists():
        documento = get_object_or_404(Documento, equipo=equipo, tipo=tipo)
        if documento.archivo:
            filepath = documento.archivo.file.name
        else:
            filepath = MEDIA_ROOT + "formularios/documento_sin_respaldo.pdf"
    else:
        filepath = MEDIA_ROOT + "formularios/documento_sin_respaldo.pdf"

    return FileResponse(open(filepath, 'rb'))
