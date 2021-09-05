#!/usr/bin/env python3 
# from fpdf import FPDF
# import libreriaCartas  
# from .libreriaCartas import *
import io
from datetime import date
from django.http import FileResponse
from fpdf import FPDF


def docReporteEstudiante(buffer, estudiante, usuario_solicitante):
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

    def fecha_left():
        meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        hoy = date.today()
        dia = hoy.day.__str__()
        mes = meses[hoy.month - 1]
        year = hoy.year.__str__()
        pdf.cell(0,0,txt='La Paz, ' + dia + ' de ' + mes + ' del ' + year, ln=1, border=0, align="L")
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

    def text_left_lista(texto_lista):
        for texto in texto_lista:
            pdf.cell(0,0,txt=texto+' ', ln=1, border=0, align="L")
            pdf.ln(th)

    def negrilla():
        pdf.set_font("Times", 'B', size=12)
        pdf.set_font("Times", size=12)

    def negrilla_subrayado():
        pdf.set_font("Times", 'BU', size=12)
        pdf.set_font("Times", size=12)

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
    
    def titulo(texto):
        pdf.set_font("Times", 'B', size=14)
        pdf.cell(0,0,txt=texto.upper(), ln=1, border=0, align="C")
        pdf.set_font("Times", size=12)
        pdf.ln(th)

    def texto_negrilla(texto):
        pdf.set_font("Times", 'B', size=12)
        pdf.cell(0,0,txt=texto, ln=1, border=0, align="J")
        pdf.set_font("Times", size=12)
        pdf.ln(th)

# totos estos datos vienen de la base de datos
# ===========================================
    nombre_estudiante = estudiante.__str__()
    carnet_est = estudiante.carnet
    extension_est = estudiante.extension
    registro_est = estudiante.registro_uni
    celular_est = estudiante.celular
    correo_est = estudiante.correo
    celular_tutor = estudiante.tutor.celular
    correo_tutor = estudiante.tutor.correo
    progreso_est = estudiante.progreso.nivel.__str__()
    docente = estudiante.grupo_doc.__str__()
    grupo_docente = estudiante.grupo_doc.grupo
    tutor = estudiante.tutor.__str__()
    usuario = usuario_solicitante.first_name + ' ' + usuario_solicitante.last_name
    correo_usuario= usuario_solicitante.email
# estatico, no se mueve, a menos que sea por personalizacion
# ******************** INICIO DEL DOCUMENTO *******************
# Titulo 
    titulo('reporte etn-1040 proyecto de grado')
    titulo('estudiante')
    titulo(nombre_estudiante)
    linea()
# Datos del estudiante
    texto_negrilla('Datos del Estudiante:')
    text_left('Nombre completo: '+nombre_estudiante)
    text_left('Cedula de Identidad: '+ carnet_est +' '+ extension_est)
    text_left('Registro Universitario: '+ registro_est)
    linea()

# Datos de contacto
    texto_negrilla('Datos de contacto:')
    text_left('Número de celular: '+ celular_est)
    text_left('Correo Electrónico: '+ estudiante.correo)
    linea()

# Estado actual etn1040
    texto_negrilla('Estado Actual ETN-1040:')
    text_left('Docente ETN-1040: '+ docente)
    text_left('Grupo: '+ grupo_docente)
    text_left('Tutor: '+ tutor)
    text_left('Progreso ETN-1040: '+ progreso_est + '% avanzado')
    linea()
# Actividades concluidas
    texto_negrilla('Actividades Elaboradas: ')
    pasos = {
            'Paso 1':['Conocimiento de Reglamentos de Proyecto de Grado',
                    'Revisión y estudio del material compartido por Docente'],
            'Paso 2':['Búsqueda de Proyectos de Grado'],
            'Paso 3':['Asignación de Tutor de Proyecto de Grado',
                    'Carta aceptación de Tutoría'],
            'Paso 4':['Entrega y revisión de Perfil de Proyecto de Grado',
                    'Registro de Perfil de Proyecto de Grado',
                    'Registro de Cronograma de Proyecto de Grado',
                    'Formulario 1'],
            'Paso 5':['Cumplir con el cronograma',
                    'Revisión del Proyecto de Grado',
                    'Registro del Proyecto de Grado',],
            'Paso 6':['Carta de Conclusión',
                'Gegeración de los 3 formularios']
            }
    progreso = int(progreso_est)
    if progreso < 14:
        text_left_lista(pasos['Paso 1'])
        texto_negrilla('Actividades Faltantes: ')
        text_left_lista(pasos['Paso 2'])
        text_left_lista(pasos['Paso 3'])
        text_left_lista(pasos['Paso 4'])
        text_left_lista(pasos['Paso 5'])
        text_left_lista(pasos['Paso 6'])
    elif progreso < 21:
        text_left_lista(pasos['Paso 1'])
        text_left_lista(pasos['Paso 2'])
        texto_negrilla('Actividades Faltantes: ')
        text_left_lista(pasos['Paso 3'])
        text_left_lista(pasos['Paso 4'])
        text_left_lista(pasos['Paso 5'])
        text_left_lista(pasos['Paso 6'])
    elif progreso < 35:
        text_left_lista(pasos['Paso 1'])
        text_left_lista(pasos['Paso 2'])
        text_left_lista(pasos['Paso 3'])
        texto_negrilla('Actividades Faltantes: ')
        text_left_lista(pasos['Paso 4'])
        text_left_lista(pasos['Paso 5'])
        text_left_lista(pasos['Paso 6'])
    elif progreso < 64:
        text_left_lista(pasos['Paso 1'])
        text_left_lista(pasos['Paso 2'])
        text_left_lista(pasos['Paso 3'])
        text_left_lista(pasos['Paso 4'])
        texto_negrilla('Actividades Faltantes: ')
        text_left_lista(pasos['Paso 5'])
        text_left_lista(pasos['Paso 6'])
    elif progreso < 86:
        text_left_lista(pasos['Paso 1'])
        text_left_lista(pasos['Paso 2'])
        text_left_lista(pasos['Paso 3'])
        text_left_lista(pasos['Paso 4'])
        text_left_lista(pasos['Paso 5'])
        texto_negrilla('Actividades Faltantes: ')
        text_left_lista(pasos['Paso 6'])
    elif progreso <= 100:
        text_left_lista(pasos['Paso 1'])
        text_left_lista(pasos['Paso 2'])
        text_left_lista(pasos['Paso 3'])
        text_left_lista(pasos['Paso 4'])
        text_left_lista(pasos['Paso 5'])
        text_left_lista(pasos['Paso 6'])
        texto_negrilla('Actividades Faltantes: ')
    
# firma usuario solicitante.
    linea(4)
    text_center('Atte.: '+ usuario)
    # text_center('Cel.: '+ celular_usuario)
    text_center('e-mail.: '+ correo_usuario)

# Fecha
    linea(2)
    fecha_left()
    guardar(buffer)

def docReporteIndicacionTutor(buffer, estudiante):
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

    def fecha_left():
        meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        hoy = date.today()
        dia = hoy.day.__str__()
        mes = meses[hoy.month - 1]
        year = hoy.year.__str__()
        pdf.cell(0,0,txt='La Paz, ' + dia + ' de ' + mes + ' del ' + year, ln=1, border=0, align="L")
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

    def text_left_lista(texto_lista):
        for texto in texto_lista:
            pdf.cell(0,0,txt=texto+' ', ln=1, border=0, align="L")
            pdf.ln(th)

    def negrilla():
        pdf.set_font("Times", 'B', size=12)
        pdf.set_font("Times", size=12)

    def negrilla_subrayado():
        pdf.set_font("Times", 'BU', size=12)
        pdf.set_font("Times", size=12)

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
    
    def titulo(texto):
        pdf.set_font("Times", 'B', size=14)
        pdf.cell(0,0,txt=texto.upper(), ln=1, border=0, align="C")
        pdf.set_font("Times", size=12)
        pdf.ln(th)

    def texto_negrilla(texto):
        pdf.set_font("Times", 'B', size=12)
        pdf.cell(0,0,txt=texto, ln=1, border=0, align="J")
        pdf.set_font("Times", size=12)
        pdf.ln(th)

# totos estos datos vienen de la base de datos
# ===========================================
    nombre_estudiante = estudiante.__str__()
    carnet_est = estudiante.carnet
    extension_est = estudiante.extension
    registro_est = estudiante.registro_uni
    celular_est = estudiante.celular
    correo_est = estudiante.correo
    celular_tutor = estudiante.tutor.celular
    correo_tutor = estudiante.tutor.correo
    progreso_est = estudiante.progreso.nivel.__str__()
    docente = estudiante.grupo_doc.__str__()
    grupo_docente = estudiante.grupo_doc.grupo
    tutor = estudiante.tutor.__str__()
    usuario = 'nadie'
    correo_usuario= 'fdsa'
# estatico, no se mueve, a menos que sea por personalizacion
# ******************** INICIO DEL DOCUMENTO *******************
# Titulo 
    titulo('ingreso al sistema para el tutor')
    titulo(nombre_estudiante)
    linea()
# Datos del estudiante
    parrafo('El estudiante: '+nombre_estudiante + ' solicito su tutoría. Para aceptar o rechazar la solicitud debe ingresar al sistema con el siguiente usuario y contraseña.')
    linea(3)
# Usuario y password
    text_left('Usuario: '+ estudiante.tutor.usuario.__str__())    
    text_left('Contraseña: '+ estudiante.tutor.usuario.__str__())    
# firma usuario solicitante.
    linea(4)
    text_center('Atte.: '+ nombre_estudiante)
    text_center('Cel.: '+ celular_est)
    text_center('e-mail.: '+ correo_est)

# Fecha
    linea(2)
    fecha_left()
    guardar(buffer)

def docReporteIndicacionTutorEnSistema(buffer, estudiante):
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

    def fecha_left():
        meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        hoy = date.today()
        dia = hoy.day.__str__()
        mes = meses[hoy.month - 1]
        year = hoy.year.__str__()
        pdf.cell(0,0,txt='La Paz, ' + dia + ' de ' + mes + ' del ' + year, ln=1, border=0, align="L")
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

    def text_left_lista(texto_lista):
        for texto in texto_lista:
            pdf.cell(0,0,txt=texto+' ', ln=1, border=0, align="L")
            pdf.ln(th)

    def negrilla():
        pdf.set_font("Times", 'B', size=12)
        pdf.set_font("Times", size=12)

    def negrilla_subrayado():
        pdf.set_font("Times", 'BU', size=12)
        pdf.set_font("Times", size=12)

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
    
    def titulo(texto):
        pdf.set_font("Times", 'B', size=14)
        pdf.cell(0,0,txt=texto.upper(), ln=1, border=0, align="C")
        pdf.set_font("Times", size=12)
        pdf.ln(th)

    def texto_negrilla(texto):
        pdf.set_font("Times", 'B', size=12)
        pdf.cell(0,0,txt=texto, ln=1, border=0, align="J")
        pdf.set_font("Times", size=12)
        pdf.ln(th)

# totos estos datos vienen de la base de datos
# ===========================================
    nombre_estudiante = estudiante.__str__()
    carnet_est = estudiante.carnet
    extension_est = estudiante.extension
    registro_est = estudiante.registro_uni
    celular_est = estudiante.celular
    correo_est = estudiante.correo
    celular_tutor = estudiante.tutor.celular
    correo_tutor = estudiante.tutor.correo
    progreso_est = estudiante.progreso.nivel.__str__()
    docente = estudiante.grupo_doc.__str__()
    grupo_docente = estudiante.grupo_doc.grupo
    tutor = estudiante.tutor.__str__()
    usuario = 'nadie'
    correo_usuario= 'fdsa'
# estatico, no se mueve, a menos que sea por personalizacion
# ******************** INICIO DEL DOCUMENTO *******************
# Titulo 
    titulo('ingreso al sistema para el tutor')
    titulo(nombre_estudiante)
    linea()
# Datos del estudiante
    parrafo('El estudiante: '+nombre_estudiante + ' solicito su tutoría. Para aceptar o rechazar la solicitud debe ingresar al sistema con el siguiente usuario y contraseña.')
    linea(3)
# Usuario y password
    text_left('Usuario: '+ estudiante.tutor.usuario.__str__())    
    text_left('Contraseña: '+ estudiante.tutor.usuario.__str__())    
# firma usuario solicitante.
    linea(4)
    text_center('Atte.: '+ nombre_estudiante)
    text_center('Cel.: '+ celular_est)
    text_center('e-mail.: '+ correo_est)

# Fecha
    linea(2)
    fecha_left()
    guardar(buffer)


