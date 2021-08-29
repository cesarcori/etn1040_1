#!/usr/bin/env python3 
# from fpdf import FPDF
# import libreriaCartas  
# from .libreriaCartas import *
import io
from datetime import date
from django.http import FileResponse
from fpdf import FPDF

def reporte_tutor_acepto(buffer, estudiante):
    pdf = FPDF(format="letter")
    pdf.add_page()
    pdf.set_font("Times", size=12)
# margen
    pdf.set_margin(25)
# Get default margins
    left = pdf.l_margin
    right = pdf.r_margin
    top = pdf.t_margin
    bottom = pdf.b_margin
# Effective page width and height
    epw = pdf.w - left - right
    eph = pdf.h - top - bottom
# salto de linea
    th = pdf.font_size * 1.2
    def fecha_right():
        meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        hoy = date.today()
        dia = hoy.day.__str__()
        mes = meses[hoy.month - 1]
        year = hoy.year.__str__()
        pdf.cell(0,0,txt='La Paz, ' + dia + ' de ' + mes + ' del ' + year, ln=1, border=0, align="R")
        pdf.ln(th)

    def text_left(text):
        pdf.cell(0,0,txt=text+' ', ln=1, border=0, align="L")
        pdf.ln(th)

    def text_right(text):
        pdf.cell(0,0,txt=text+' ', ln=1, border=0, align="R")
        pdf.ln(th)

    def text_center(text):
        pdf.cell(0,0,txt=text, ln=1, border=0, align="C")
        pdf.ln(th)

    def negrilla():
        pdf.set_font("Times", 'B', size=12)

    def negrilla_subrayado():
        pdf.set_font("Times", 'BU', size=12)

    def linea(numero_lineas=1):
        for n in range(numero_lineas):
            pdf.ln(th)

    def normal():
        pdf.set_font("Times", size=12)

    def guardar(nombre_archivo):
        pdf.output(nombre_archivo)

    def parrafo(parrafo):
        pdf.write(th, parrafo + ' ')

    def justificado(parrafo):
        pdf.multi_cell(0,th,txt=parrafo, ln=1, border=0, align="J")
        pdf.ln(th)
# totos estos datos vienen de la base de datos
# ===========================================
    nombre_estudiante = estudiante.__str__()
    celular_tutor = estudiante.tutor.celular
    correo_tutor = estudiante.tutor.correo
    docente = estudiante.grupo_doc.__str__()
    tutor = estudiante.tutor.__str__()
    titulo_perfil= ''
# estatico, no se mueve, a menos que sea por personalizacion
    cargo = 'docente de la asignatura etn-1040'
    lugar = 'carrera de ingeniería electrónica'
    institucion = 'facultad de ingeniería'
    universidad = 'universidad mayor de san andrés'
    parrafo1_1 = 'Mediante la presente deseo poner en conocimiento suyo, mi aceptación como tutor, en el desarrollo del Proyecto de Grado'
    parrafo1_2 = titulo_perfil
    parrafo1_3 = 'a cargo del estudiante'
    parrafo1_4 = nombre_estudiante
    parrafo1_5 = 'Y doy el compromiso de supervisar el cumplimiento de cronograma propuesto en el perfil.'
    despedida = 'Sin otro particular, me despido con las consideraciones más distinguitas'

# Fecha
    fecha_right()
    linea(2)
# Dirigido:
    text_left('Señor')
    text_left('Ing. '+ docente )
    negrilla()
    text_left(cargo.upper())
    text_left(lugar.upper())
    text_left(institucion.upper())
    text_left(universidad.upper())
    linea()
    normal()
    text_left('Presente.-')
    linea()
    text_left('De mi concideración:')
    linea()

# parrafo
    parrafo(parrafo1_1)    
    negrilla()
    # parrafo(parrafo1_2)
    normal()
    parrafo(parrafo1_3)
    negrilla()
    parrafo(parrafo1_4+'.')
    normal()
    parrafo(parrafo1_5)

# despedida
    linea(3)
    text_left(despedida)
    linea()

# firma 
    linea(17)
    text_center('Ing.: '+tutor)
    text_center('Cel.: '+ celular_tutor)
    text_center('e-mail.: '+ correo_tutor)
    guardar(buffer)


