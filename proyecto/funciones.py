#!/usr/bin/env python3 
# from fpdf import FPDF
# import libreriaCartas  
# from .libreriaCartas import *
from datetime import date, timedelta
from django.http import FileResponse
from .models import ActividadesCronograma, DatosEstudiante, RegistroPerfil

def infoCronograma(id_est):
    estudiante = DatosEstudiante.objects.get(id=id_est)
    cronograma_existe = ActividadesCronograma.objects.filter(usuario=estudiante).exists()
    if cronograma_existe:
        cronograma = ActividadesCronograma.objects.filter(usuario=estudiante)
            # fecha de registro del cronograma o fecha de registro del proyecto
        fecha = RegistroPerfil.objects.get(usuario=estudiante).fecha_creacion
            # fecha limite sistema 2 años y medio
        # prueba modificar el 0 del delta para eliminar al usuario
        fecha = fecha.date()#-timedelta(0)
        fecha_limite_sistema = fecha+ timedelta(365*2.5)
        dia_restante_sistema = fecha_limite_sistema - date.today()
        dia_restante_sistema = dia_restante_sistema.days
        # fecha transcurrida desde el inicio
        dias_transcurridos = date.today() - fecha
        dias_transcurridos = dias_transcurridos + timedelta(0)
        # dias a semanas:
        semanas = dias_transcurridos.days // 7# - 1
        num_semana = dias_transcurridos.days // 7 + 1
        dias = dias_transcurridos.days % 7
        dias_transcurridos = dias_transcurridos.days# - 7
        # duracion del proyecto
        max_semana = range(1,1+max([n.semana_final for n in cronograma]))
        semana_total = len(max_semana)
        dia_total = 7*semana_total
        # fecha limite cronograma
        fecha_limite_crono = fecha + timedelta(dia_total)
        dia_restante_crono = fecha_limite_crono - date.today()
        dia_restante_crono = dia_restante_crono.days
        # fecha limite sistema 2 años y medio
        fecha_limite_sistema = fecha + timedelta(365*2.5)
        dia_restante_sistema = fecha_limite_sistema - date.today()
        dia_restante_sistema= dia_restante_sistema.days
        # porcentaje
        por_dia_crono = (dia_restante_crono* 100) / dia_total
        por_dia_sistema = dia_restante_sistema* 100 / (365*2.5)
        por_dia_crono = str(por_dia_crono)
        por_dia_sistema = str(por_dia_sistema)

        dia_retrazo = dia_restante_crono * -1
        por_dia_retrazo = ( dia_restante_crono *-1* 100)/(365*2.5-dia_total) 
        por_dia_retrazo= str(por_dia_retrazo)

        if num_semana <= semana_total:
            limite_cronograma = False
        else:
            actividades = []
            limite_cronograma = True
        if dia_restante_sistema <= -1:
            estudiante.usuario.delete()
            print('Se jodio')
            return HttpResponse("Fuiste Eliminado del sistema.")
    else:
        dia_restante_crono = ''
        dia_restante_sistema = ''
        dia_retrazo = ''
        semana_total = ''
        por_dia_crono = ''
        por_dia_sistema = ''
        por_dia_retrazo = ''
        limite_cronograma = ''
    context = {
                'dia_restante_crono':dia_restante_crono,
                'dia_restante_sistema':dia_restante_sistema,
                'dia_retrazo':dia_retrazo,
                'semana_total':semana_total,
                'por_dia_crono':por_dia_crono,
                'por_dia_sistema':por_dia_sistema,
                'por_dia_retrazo':por_dia_retrazo,
                'limite_cronograma':limite_cronograma,
                'cronograma_existe':cronograma_existe,
            'dia_restante_sistema':dia_restante_sistema}
    return context
