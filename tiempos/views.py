from django.shortcuts import render, get_object_or_404

from datetime import date, timedelta

from revisar_documentos.models import SalaDocumentoDoc, SalaRevisarDoc
from proyecto.models import Equipo

def resumen(request, pk):
    grupo = request.user.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)
    salas = SalaDocumentoDoc.objects.filter(equipo=equipo).order_by('-fecha_creacion')
    # el total de salas que se puede tener son 6 maximo.
    dicc_salaDoc_days = {}
    for sala in salas:
        if sala.salarevisardoc_set.first():
            fecha_presentacion = sala.salarevisardoc_set.first().fecha_creacion
            fecha_visto_bueno = sala.updated
            if sala.visto_bueno:
                duration = fecha_visto_bueno - fecha_presentacion
                dicc_salaDoc_days[sala] = duration.days
            else:
                duration = date.today() - fecha_presentacion.astimezone().date()
                dicc_salaDoc_days[sala] = duration.days
        else:
            # print('aun no se empezo ninguna revision')
            pass
    
    context = {'grupo':grupo, 'equipo':equipo,'dicc_salaDoc_days': dicc_salaDoc_days}
    return render(request, 'tiempos/resumen.html', context)
