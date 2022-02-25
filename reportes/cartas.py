#!/usr/bin/env python3 
# from fpdf import FPDF
# import libreriaCartas  
# from .libreriaCartas import *
import io
from datetime import date
from django.http import FileResponse
from fpdf import FPDF
from etn1040_1.settings import MEDIA_ROOT
from proyecto.models import Documentos
# from .libreriaCartas import *

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
# ===========================================
# de la base de datos
# ===========================================
    nombre_estudiante = estudiante.__str__()
    celular_tutor = estudiante.equipo.tutor.celular
    correo_tutor = estudiante.equipo.tutor.correo
    docente = estudiante.grupo_doc.__str__()
    tutor = estudiante.equipo.tutor.__str__()
    titulo_perfil= ''
# estatico, no se mueve, a menos que sea por personalizacion
    cargo = 'docente de la asignatura etn-1040'
    lugar = 'carrera de ingeniería electrónica'
    institucion = 'facultad de ingeniería'
    universidad = 'universidad mayor de san andrés'
    parrafo1_1 = 'Mediante la presente deseo poner en conocimiento suyo, mi aceptación como tutor, en el desarrollo del Proyecto de Grado'
    parrafo1_2 = titulo_perfil
    if estudiante.equipo.cantidad > 1:
        parrafo1_3 = 'de los estudiantes'
        integrantes = [n.__str__() for n in estudiante.equipo.datosestudiante_set.all()]
        parrafo1_4 = ", ".join(integrantes)
    else:
        parrafo1_3 = 'del estudiante'
        parrafo1_4 = nombre_estudiante
    parrafo1_5 = 'dando el compromiso de supervisar el cumplimiento de cronograma propuesto en el perfil.'
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
    parrafo(parrafo1_2)
    normal()
    parrafo(parrafo1_3)
    negrilla()
    # parrafo(parrafo1_4+'.')
    # if estudiante.equipo.cantidad > 1:
        # for parrafo1_4 in integrantes:
            # parrafo(parrafo1_4+', ')
    # else:
        # parrafo(parrafo1_4+', ')

    parrafo(parrafo1_4+', ')
    normal()
    parrafo(parrafo1_5)

# despedida
    linea(3)
    text_left(despedida)
    linea()

# firma     

    linea(17)

    if Documentos.objects.filter(usuario=estudiante.equipo.tutor.usuario).exists():
        if estudiante.equipo.tutor.usuario.documentos.firma_carta_aceptacion:
            name = MEDIA_ROOT+estudiante.equipo.tutor.firma.name
            pdf.image(name, x = 85, y = 190, w = 50)
    text_center('Ing.: '+tutor)
    text_center('Cel.: '+ celular_tutor)
    text_center('e-mail.: '+ correo_tutor)
    guardar(buffer)

def carta_aceptacion(buffer, estudiante):
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
    # nombre = 'Julio Cesar Cori Ochoa'
    # carnet = '6002358'
    # extension = 'L.P.'
    # celular = '73009217'
    # correo = 'ingeumsacori@gmail.com'
    # docente = 'Jorge Mario León Gómez'
    # tutor = 'Freddy Valle Velasquez'
    # titulo_perfil = 'Diseño e implementación de un sistema de información para el seguimiento y administración de proyectos de grado para la materia ETN-1040. '
# ===========================================
# de la base de datos
# ===========================================
    # nombre = info_estu[0]
    # carnet = info_estu[1] 
    # extension = info_estu[2] 
    # celular = info_estu[3] 
    # correo = info_estu[4] 
    # docente = info_estu[5] 
    # tutor = info_estu[6] 
    # titulo_perfil = info_estu[7] 
# ===========================================
    nombre_estudiante = estudiante.__str__()
    celular_tutor = estudiante.equipo.tutor.celular
    correo_tutor = estudiante.equipo.tutor.correo
    docente = estudiante.grupo_doc.__str__()
    tutor = estudiante.equipo.tutor.__str__()
    titulo_perfil= estudiante.registroperfil.titulo
# estatico, no se mueve, a menos que sea por personalizacion
    cargo = 'docente de la asignatura etn-1040'
    lugar = 'carrera de ingeniería electrónica'
    institucion = 'facultad de ingeniería'
    universidad = 'universidad mayor de san andrés'
    parrafo1_1 = 'Mediante la presente deseo poner en conocimiento suyo, mi aceptación como tutor, en el desarrollo del Proyecto de Grado:'
    parrafo1_2 = titulo_perfil
    parrafo1_3 = 'A cargo del estudiante'
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
    parrafo(parrafo1_2)
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
    ruta_firma='firma.jpg'
    fpdf.image(x = None, y = None, w = 0, h = 0, link = ruta_firma)
    text_center('Ing.: '+tutor)
    text_center('Cel.: '+ celular_tutor)
    text_center('e-mail.: '+ correo_tutor)
    guardar(buffer)

def carta_solicitud(buffer, info_estu):
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
    # nombre = 'Julio Cesar Cori Ochoa'
    # carnet = '6002358'
    # extension = 'L.P.'
    # celular = '73009217'
    # correo = 'ingeumsacori@gmail.com'
    # docente = 'Jorge Mario León Gómez'
    # tutor = 'Freddy Valle Velasquez'
    # cargo = 'director'
    # lugar = 'instituto de electrónica aplicada'
    # institucion = 'facultad de ingeniería'
# ===========================================
# de la base de datos
# ===========================================
    nombre = info_estu[0]
    carnet = info_estu[1]
    extension = info_estu[2]
    celular = info_estu[3]
    correo = info_estu[4]
    docente = info_estu[5]
    tutor = info_estu[6]
    cargo = info_estu[7]
    lugar = info_estu[8]
    institucion = info_estu[9]
# ===========================================
    parrafo1_1 = 'Saludo a usted de mi mayor concideración y con todo respeto '
    parrafo1_2 = 'solicitar tutoría en la elaboración del Proyecto de Grado '
    parrafo1_3 = 'para la Carrera de Ingeniería Electrónica, Facultad de Ingeniería, Universidad Mayor de San Andrés.'
    parrafo4 = 'Debido a su gran colaboración, ideas y atención que me brinda para la elaboración del trabajo. Su conocimiento y experiencias son de vital importancia para el desarrollo del Proyecto de Grado, así como sus concejos y orientaciones.'
    despedida = 'Sin otro particular, me despido con las consideraciones más distinguidas.'
# Fecha
    fecha_right()
    linea()
# Dirigido:
    text_left('Señor')
    text_left('Ing. '+ tutor )
    negrilla()
    text_left(cargo.upper())
    text_left(lugar.upper())
    text_left(institucion.upper())
    linea()
    normal()
    text_left('Presente.-')
    linea()
    negrilla_subrayado()
    text_right('Ref.- SOLICITUD DE TUTORÍA')
    linea(2)

    normal()
    text_left('De mi concideración:')
    linea()

    parrafo(parrafo1_1)
    negrilla()
    parrafo(parrafo1_2)
    normal()
    parrafo(parrafo1_3)
    linea(2)
    justificado(parrafo4)
    linea()

# despedida 
    parrafo(despedida)
    linea(17)

# firma 
    text_center('Univ.: '+nombre)
    text_center('C.I.: '+carnet+' '+ extension)
    text_center('Cel.: '+ celular)
    text_center('e-mail.: '+ correo)

# guardar documento
    guardar(buffer)

def generarCartaFinal(buffer, equipo):
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
    estudiante = equipo.datosestudiante_set.first()
    nombre = estudiante.__str__()
    celular_tutor = equipo.tutor.celular
    correo_tutor = equipo.tutor.correo
    docente = equipo.docente.__str__()
    tutor = equipo.tutor.__str__()
    # titulo_proyecto = estudiante.proyectodegrado.titulo
    titulo_proyecto = equipo.registroperfil.titulo

    if estudiante.equipo.cantidad > 1:
        parrafo1_3 = 'de los estudiantes'
        integrantes = [n.__str__() for n in estudiante.equipo.datosestudiante_set.all()]
        parrafo1_4 = ", ".join(integrantes)
    else:
        parrafo1_3 = 'del estudiante'
        parrafo1_4 = nombre_estudiante

# ===========================================
# estatico, no se mueve, a menos que sea por personalizacion
    cargo = 'docente de la asignatura etn-1040'
    lugar = 'carrera de ingeniería electrónica'
    institucion = 'facultad de ingeniería'
    universidad = 'universidad mayor de san andrés'
    parrafo1_1 = 'Mediante la presente deseo poner en conocimiento suyo, la conclusión satisfactoria, en el desarrollo del Proyecto de Grado:'
    parrafo1_2 = titulo_proyecto
    # parrafo1_3 = 'A cargo del estudiante'
    # parrafo1_4 = nombre
    parrafo1_5 = 'Doy total conformidad al mencionado Proyecto de Grado que cuenta con las características necesarias para ser defendido y presentado ante el Tribunal de Docentes.'
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
    parrafo(parrafo1_2)
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
    if Documentos.objects.filter(usuario=estudiante.equipo.tutor.usuario).exists():
        if estudiante.equipo.tutor.usuario.documentos.firma_carta_aceptacion:
            name = MEDIA_ROOT+estudiante.equipo.tutor.firma.name
            pdf.image(name, x = 85, y = 195, w = 50)
    text_center('Ing.: '+tutor)
    text_center('Cel.: '+ celular_tutor)
    text_center('e-mail.: '+ correo_tutor)
    guardar(buffer)

