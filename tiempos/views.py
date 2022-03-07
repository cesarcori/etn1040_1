from django.shortcuts import render, get_object_or_404

from datetime import date, timedelta

from revisar.models import SalaDocumentoApp, SalaRevisarApp
from proyecto.models import Equipo

def resumen(request, pk):
    grupo = request.user.groups.get().name
    equipo = get_object_or_404(Equipo, id=pk)
    salas = SalaDocumentoApp.objects.filter(equipo=equipo)
    # el total de salas que se puede tener son 6 maximo.
    for sala in salas:
        if sala.salarevisarapp_set.first():
            fecha_presentacion = sala.salarevisarapp_set.first().fecha_creacion
            if sala.visto_bueno:
                fecha_visto_bueno = sala.updated
                duration = fecha_visto_bueno - fecha_presentacion
                print(duration.days)
            else:
                print('aun no se dio visto bueno')
        else:
            print('aun no se empezo ninguna revision')
    
    # fecha de primera presentacion
    # fecha de visto bueno.
    context = {'grupo':grupo, 'equipo':equipo}
    return render(request, 'tiempos/resumen.html', context)
