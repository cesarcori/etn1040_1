#!/usr/bin/env python3 
# from fpdf import FPDF
# import libreriaCartas  
# from .libreriaCartas import *
import io
from datetime import date
from django.http import FileResponse
from fpdf import FPDF


def generarReporteEstudiante(buffer, estudiante, usuario_solicitante):
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
    celular_tutor = estudiante.equipo.tutor.celular
    correo_tutor = estudiante.equipo.tutor.correo
    progreso_est = estudiante.progreso.nivel.__str__()
    docente = estudiante.grupo_doc.__str__()
    grupo_docente = estudiante.grupo_doc.grupo
    tutor = estudiante.equipo.tutor.__str__()
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

def generarReporteIndicacionTutor(buffer, estudiante, http_host):
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
    integrantes = estudiante.equipo.datosestudiante_set.all()
    estudiantes= [e.__str__() for e in integrantes]
    nombre_estudiantes = " - ".join(estudiantes)
    celular_est = estudiante.celular
    correo_est = estudiante.correo
    tutor = estudiante.equipo.tutor.__str__()
    celular_tutor = estudiante.equipo.tutor.celular
    correo_tutor = estudiante.equipo.tutor.correo
    # carnet_est = estudiante.carnet
    # extension_est = estudiante.extension
    # registro_est = estudiante.registro_uni
    # docente = estudiante.grupo_doc.__str__()
    # grupo_docente = estudiante.grupo_doc.grupo
# estatico, no se mueve, a menos que sea por personalizacion
# ******************** INICIO DEL DOCUMENTO *******************
# Titulo 
    titulo('ingreso al sistema para el tutor')
    titulo(correo_tutor)
    linea()
# Datos del estudiante
    if integrantes.count() > 1:
        parte_nombre = f"Los estudiantes: {nombre_estudiantes}"
    else:
        parte_nombre = f"El estudiante: {nombre_estudiantes}"
    parrafo(parte_nombre + ' solicito su tutoría. Para aceptar la solicitud debe ingresar al sistema mediante URL: '+ http_host + ' con el siguiente usuario y contraseña.')
    linea(3)
# Usuario y password
    text_left('Usuario: '+ estudiante.equipo.tutor.usuario.__str__())    
    text_left('Contraseña: '+ estudiante.equipo.tutor.usuario.__str__())    
# firma usuario solicitante.
    for estudiante in integrantes:
        linea(3)
        text_center('Atte.: '+ estudiante.__str__())
        text_center('Cel.: '+ estudiante.celular)
        text_center('e-mail.: '+ estudiante.correo)

# Fecha
    linea(2)
    fecha_left()
    guardar(buffer)

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
# from proyecto.models import MensajeTutorRevisarProyecto
def generarFirmaTutorCapitulos(buffer, equipo):
    # doc = SimpleDocTemplate(buffer, pagesize=letter)
    def fecha():
        meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        hoy = date.today()
        dia = hoy.day.__str__()
        mes = meses[hoy.month - 1]
        year = hoy.year.__str__()
        fecha_hoy = dia + ' de ' + mes + ' del ' + year
        return fecha_hoy
    def fecha_mes(fecha):
        meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        year_mes_dia = fecha.split('-')
        year = year_mes_dia[0]
        mes = meses[int(year_mes_dia[1])- 1]
        dia = year_mes_dia[2]
        fecha_cadena = dia + ' de ' + mes + ' del ' + year
        return fecha_cadena

    styleSheet = getSampleStyleSheet()

    doc = SimpleDocTemplate(buffer, pagesize=letter,leftMargin=10,
        rightMargin=10,topMargin=20,bottomMargin=20)
    story = []
    style = styleSheet['BodyText']

    header = Paragraph("<para align=center><b><font size=12>Plantilla de Avance</font></b></para>", style)

    # p = Paragraph('* ' +'''La referencia bibliografica debe estar de acuerdo con 
    # las nomas apa ademas se seguir escribiendo. trabajando \n mas'''+'* '+ '''otro parrafo
    # de esos largos que no queda otra que aumentar''',style)

    nombre_estudiante = equipo.datosestudiante_set.first().__str__()
    if equipo.cantidad > 1:
        valor = 'Estudiantes'
    else:
        valor = 'Estudiante'
    nombres = [f"{n.__str__()}" for n in equipo.datosestudiante_set.all()]
    nombres_estudiantes = " - ".join(nombres)
    nombre_tutor = equipo.tutor.__str__()
    titulo_perfil = equipo.registroperfil.titulo.upper()
    # salas = estudiante.salarevisarproyecto_set.all()
    sala_doc_tutor = equipo.saladocumentoapp_set.get(tipo='proyecto', revisor=equipo.tutor.usuario)
    salas_revisar = sala_doc_tutor.salarevisarapp_set.all()
    lista_estudiantes = f"<b>{valor}:</b> {nombres_estudiantes}"
    data1 = [
        [header,'','',''],                    
        # [Paragraph('<b>Estudiante: </b>'+nombre_estudiante), '',Paragraph('<b>Tutor: </b>Ing. '+nombre_tutor),''],
        [Paragraph('<b>Tutor: </b>Ing. '+nombre_tutor),'','',''],
        # [Paragraph('<b>'+plural_est+': </b>'+nombre_estudiante), '','',''],
        [Paragraph(lista_estudiantes), '','',''],
        [Paragraph('<b>Proyecto de Grado: </b>'+titulo_perfil),'','',''],
        ['Tema','Fecha','Firma Tutor','Observaciones'],
    ]
    # generacion de las observaciones
    data2 = []
    for sala in salas_revisar:
        mensajes_tut = sala.mensajerevisarapp_set.filter(usuario=equipo.tutor.usuario)
        observaciones = []
        for mensaje in mensajes_tut:
            # observacion = mensaje.texto
            observacion = mensaje.mensaje
            observaciones.append('*'+observacion)
            enter = "<br/><br/>"
            obs_union = enter.join(observaciones)
            obs_parrafo = Paragraph(obs_union)
        # en el caso que no exista observaciones por el tutor
        if mensajes_tut:
            fecha_ultima_obs = mensajes_tut[0].fecha_creacion.date().__str__()
            data_aux = [Paragraph(sala.asunto), fecha_mes(fecha_ultima_obs), '', obs_parrafo]
        else:
            fecha_ultima_obs = ''
            data_aux = ['','','','']
        data2.append(data_aux)
    data = data1 + data2

    tblstyle = TableStyle([
        # ('GRID', (0,0), (-1,-1), 0.5, colors.grey), descomentar para ver la disposicion
        ('SPAN', (0,0), (-1,0)),
        ('SPAN', (0,1), (-1,1)),
        ('SPAN', (0,2), (-1,2)),
        ('SPAN', (0,3), (-1,3)),
        # ('SPAN', (0,1), (1,1)),
        # ('SPAN', (2,1), (3,1)), # este no se por que lo puse
        # ('SPAN', (0,2), (-1,2)),
        ('INNERGRID', (0,4), (-1,-1), 0.3, colors.black),
        ('BOX', (0,4), (-1,-1), 0.3, colors.black),
        ('FONTNAME', (0,4),(-1,4),'Helvetica-Bold'),
        ('ALIGN',(0,4),(-1,-1),'CENTER'),
        ('VALIGN',(0,4),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,4),(-1,4), colors.HexColor('#f6ddea')),
    ])

    for n in range(6,len(data)+1,2):
        tblstyle.add('BACKGROUND',(0,n),(-1,n), colors.HexColor('#f6ddea'))

    t = Table(data)
    t.setStyle(tblstyle)
    story.append(t)
    # write the document to disk
    # aW = 460
    # aH = 720

    # w, h = header.wrap(aW, aH)
    # header.drawOn(canv, 72, aH)
    # aH = aH - h
    # w, h = t.wrap(aW, aH)
    # t.drawOn(canv, 72, aH-h)
    doc.build(story)



# def generarReporteCapitulos2(buffer, estudiante):
    # pdf = FPDF(format="letter")
    # pdf.add_page()
    # pdf.set_font("Times", size=12)
# # margen
    # pdf.set_margin(25)
# # Get default margins
    # left = pdf.l_margin
    # right = pdf.r_margin
    # top = pdf.t_margin
    # bottom = pdf.b_margin
# # Effective page width and height
    # epw = pdf.w - left - right
    # eph = pdf.h - top - bottom
# # salto de linea
    # th = pdf.font_size * 1.2
    # def fecha_right():
        # meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        # hoy = date.today()
        # dia = hoy.day.__str__()
        # mes = meses[hoy.month - 1]
        # year = hoy.year.__str__()
        # pdf.cell(0,0,txt='La Paz, ' + dia + ' de ' + mes + ' del ' + year, ln=1, border=0, align="R")
        # pdf.ln(th)

    # def fecha_left():
        # meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        # hoy = date.today()
        # dia = hoy.day.__str__()
        # mes = meses[hoy.month - 1]
        # year = hoy.year.__str__()
        # pdf.cell(0,0,txt='La Paz, ' + dia + ' de ' + mes + ' del ' + year, ln=1, border=0, align="L")
        # pdf.ln(th)

    # def text_left(text):
        # pdf.cell(0,0,txt=text+' ', ln=1, border=0, align="L")
        # pdf.ln(th)

    # def text_right(text):
        # pdf.cell(0,0,txt=text+' ', ln=1, border=0, align="R")
        # pdf.ln(th)

    # def text_center(text):
        # pdf.cell(0,0,txt=text, ln=1, border=0, align="C")
        # pdf.ln(th)

    # def text_left_lista(texto_lista):
        # for texto in texto_lista:
            # pdf.cell(0,0,txt=texto+' ', ln=1, border=0, align="L")
            # pdf.ln(th)

    # def negrilla():
        # pdf.set_font("Times", 'B', size=12)
        # pdf.set_font("Times", size=12)

    # def negrilla_subrayado():
        # pdf.set_font("Times", 'BU', size=12)
        # pdf.set_font("Times", size=12)

    # def linea(numero_lineas=1):
        # for n in range(numero_lineas):
            # pdf.ln(th)

    # def normal():
        # pdf.set_font("Times", size=12)
    # def guardar(nombre_archivo):
        # pdf.output(nombre_archivo)

    # def parrafo(parrafo):
        # pdf.write(th, parrafo + ' ')

    # def justificado(parrafo):
        # pdf.multi_cell(0,th,txt=parrafo, ln=1, border=0, align="J")
        # pdf.ln(th)
    
    # def titulo(texto):
        # pdf.set_font("Times", 'B', size=14)
        # pdf.cell(0,0,txt=texto.upper(), ln=1, border=0, align="C")
        # pdf.set_font("Times", size=12)
        # pdf.ln(th)

    # def texto_negrilla(texto):
        # pdf.set_font("Times", 'B', size=12)
        # pdf.cell(0,0,txt=texto, ln=1, border=0, align="J")
        # pdf.set_font("Times", size=12)
        # pdf.ln(th)

# # totos estos datos vienen de la base de datos
# # ===========================================
    # nombre_estudiante = estudiante.__str__()
    # carnet_est = estudiante.carnet
    # extension_est = estudiante.extension
    # registro_est = estudiante.registro_uni
    # celular_est = estudiante.celular
    # correo_est = estudiante.correo
    # celular_tutor = estudiante.equipo.tutor.celular
    # correo_tutor = estudiante.equipo.tutor.correo
    # progreso_est = estudiante.progreso.nivel.__str__()
    # docente = estudiante.grupo_doc.__str__()
    # grupo_docente = estudiante.grupo_doc.grupo
    # tutor = estudiante.equipo.tutor.__str__()
    # usuario = 'nadie'
    # correo_usuario= 'fdsa'
    # http_host = 'http'
# # estatico, no se mueve, a menos que sea por personalizacion
# # ******************** INICIO DEL DOCUMENTO *******************
# # Titulo 
    # titulo('Plantilla de Avance')
    # linea()
# # Datos 
    # text_left('Estudiante: ' + nombre_estudiante)
    # text_left('Tutor: ' + tutor)
    # text_left('Nombre del Proyecto: ' + estudiante.proyectodegrado.titulo )
# # Tabla
    # spacing = 1
    # letra = 3
    # data = [['First Name', 'Last Name', 'email', 'zip'],
            # ['Mike', 'Driscoll', 'mike@somewhere.com', '55555'],
            # ['John', 'Doe', 'jdoe@doe.com', '12345'],
            # ['Nina', 'Ma', 'inane@where.com', '54321']
            # ]
    # col_width = pdf.w / 4.9
    # row_height = pdf.font_size
    # for row in data:
        # for item in row:
            # pdf.cell(col_width, row_height*spacing, txt=item, border=1)
        # pdf.ln(row_height*spacing)
    # col_num = letra * 4
    # ancho = 170
    # col_1 = 50
    # col_2 = 30
    # col_3 = 30
    # col_4 = 70
    # # pdf.cell(col_num, row_height*spacing, txt='Tema',border=1)
    # pdf.cell(col_1, txt='Capitulo 1: Introduccion',border=1)
    # pdf.multi_cell(w=col_2,txt='4 de marzo\n del 2021',border=1)
    # pdf.cell(col_1, txt='Capitulo 1: Introduccion',border=1)
    # pdf.multi_cell(w=col_3,txt='Firma del tutor',border=1)
    # pdf.multi_cell(w=col_4,txt='La referencia bibliografica debe estar de',border=1)
    
# # Fecha
    # linea(2)
    # fecha_left()
    # guardar(buffer)

# def generarReporteIndicacionTutorEnSistema(buffer, estudiante):
    # pdf = FPDF(format="letter")
    # pdf.add_page()
    # pdf.set_font("Times", size=12)
# # margen
    # pdf.set_margin(25)
# # Get default margins
    # left = pdf.l_margin
    # right = pdf.r_margin
    # top = pdf.t_margin
    # bottom = pdf.b_margin
# # Effective page width and height
    # epw = pdf.w - left - right
    # eph = pdf.h - top - bottom
# # salto de linea
    # th = pdf.font_size * 1.2
    # def fecha_right():
        # meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        # hoy = date.today()
        # dia = hoy.day.__str__()
        # mes = meses[hoy.month - 1]
        # year = hoy.year.__str__()
        # pdf.cell(0,0,txt='La Paz, ' + dia + ' de ' + mes + ' del ' + year, ln=1, border=0, align="R")
        # pdf.ln(th)

    # def fecha_left():
        # meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        # hoy = date.today()
        # dia = hoy.day.__str__()
        # mes = meses[hoy.month - 1]
        # year = hoy.year.__str__()
        # pdf.cell(0,0,txt='La Paz, ' + dia + ' de ' + mes + ' del ' + year, ln=1, border=0, align="L")
        # pdf.ln(th)

    # def text_left(text):
        # pdf.cell(0,0,txt=text+' ', ln=1, border=0, align="L")
        # pdf.ln(th)

    # def text_right(text):
        # pdf.cell(0,0,txt=text+' ', ln=1, border=0, align="R")
        # pdf.ln(th)

    # def text_center(text):
        # pdf.cell(0,0,txt=text, ln=1, border=0, align="C")
        # pdf.ln(th)

    # def text_left_lista(texto_lista):
        # for texto in texto_lista:
            # pdf.cell(0,0,txt=texto+' ', ln=1, border=0, align="L")
            # pdf.ln(th)

    # def negrilla():
        # pdf.set_font("Times", 'B', size=12)
        # pdf.set_font("Times", size=12)

    # def negrilla_subrayado():
        # pdf.set_font("Times", 'BU', size=12)
        # pdf.set_font("Times", size=12)

    # def linea(numero_lineas=1):
        # for n in range(numero_lineas):
            # pdf.ln(th)

    # def normal():
        # pdf.set_font("Times", size=12)

    # def guardar(nombre_archivo):
        # pdf.output(nombre_archivo)

    # def parrafo(parrafo):
        # pdf.write(th, parrafo + ' ')

    # def justificado(parrafo):
        # pdf.multi_cell(0,th,txt=parrafo, ln=1, border=0, align="J")
        # pdf.ln(th)
    
    # def titulo(texto):
        # pdf.set_font("Times", 'B', size=14)
        # pdf.cell(0,0,txt=texto.upper(), ln=1, border=0, align="C")
        # pdf.set_font("Times", size=12)
        # pdf.ln(th)

    # def texto_negrilla(texto):
        # pdf.set_font("Times", 'B', size=12)
        # pdf.cell(0,0,txt=texto, ln=1, border=0, align="J")
        # pdf.set_font("Times", size=12)
        # pdf.ln(th)

# # totos estos datos vienen de la base de datos
# # ===========================================
    # nombre_estudiante = estudiante.__str__()
    # carnet_est = estudiante.carnet
    # extension_est = estudiante.extension
    # registro_est = estudiante.registro_uni
    # celular_est = estudiante.celular
    # correo_est = estudiante.correo
    # celular_tutor = estudiante.equipo.tutor.celular
    # correo_tutor = estudiante.equipo.tutor.correo
    # progreso_est = estudiante.progreso.nivel.__str__()
    # docente = estudiante.grupo_doc.__str__()
    # grupo_docente = estudiante.grupo_doc.grupo
    # tutor = estudiante.equipo.tutor.__str__()
    # usuario = 'nadie'
    # correo_usuario= 'fdsa'
# # estatico, no se mueve, a menos que sea por personalizacion
# # ******************** INICIO DEL DOCUMENTO *******************
# # Titulo 
    # titulo('ingreso al sistema para el tutor')
    # titulo(tutor)
    # linea()
# # Datos del estudiante
    # parrafo('El estudiante: '+nombre_estudiante + ' solicito su tutoría. Para aceptar o rechazar la solicitud debe ingresar al sistema con el siguiente usuario y contraseña.')
    # linea(3)
# # Usuario y password
    # text_left('Usuario: '+ estudiante.equipo.tutor.usuario.__str__())    
    # text_left('Contraseña: '+ estudiante.equipo.tutor.usuario.__str__())    
# # firma usuario solicitante.
    # linea(4)
    # text_center('Atte.: '+ nombre_estudiante)
    # text_center('Cel.: '+ celular_est)
    # text_center('e-mail.: '+ correo_est)

# # Fecha
    # linea(2)
    # fecha_left()
    # guardar(buffer)
