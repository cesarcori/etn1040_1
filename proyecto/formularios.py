#!/usr/bin/env python3 
from fpdf import FPDF
from os import remove
from datetime import date
import PyPDF2
from etn1040_1.settings import MEDIA_ROOT
UNIDADES = (
    'cero',
    'uno',
    'dos',
    'tres',
    'cuatro',
    'cinco',
    'seis',
    'siete',
    'ocho',
    'nueve'
)
DECENAS = (
    'diez',
    'once',
    'doce',
    'trece',
    'catorce',
    'quince',
    'dieciseis',
    'diecisiete',
    'dieciocho',
    'diecinueve'
)
VEINTE = (
    'Veinte',
    'Veintiun',
    'Veintidos',
    'Veintitres',
    'Veinticuatro',
    'Veinticinco',
    'Veintiseis',
    'Veintisiete',
    'Veintiocho',
    'Veintinueve',
)
DIEZ_DIEZ = (
    'Cero',
    'Diez',
    'Veinte',
    'Treinta',
    'Cuarenta',
    'Cincuenta',
    'Sesenta',
    'Setenta',
    'Ochenta',
    'Noventa'
)
def fecha_right():
    meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
    hoy = date.today()
    dia = hoy.day.__str__()
    mes = meses[hoy.month - 1]
    year = hoy.year.__str__()
    return dia, mes, year
def numero_letra(numero):
    numero = int(numero)
    if numero < 10:
        return UNIDADES[numero]
    decena, unidad = divmod(numero, 10)
    if numero <= 19:
        resultado = DECENAS[unidad]
    elif numero == 20:
        resultado = 'Veinte'
    elif numero == 100:
        resultado = 'Cien'
    elif numero <= 29 and numero>=21:
        resultado = 'Veinti%s' % UNIDADES[unidad]
    else:
        resultado = DIEZ_DIEZ[decena]
        if unidad > 0:
            resultado = '%s y %s' % (resultado, UNIDADES[unidad])
    return resultado
    # if numero_entero <= 99:
        # resultado = leer_decenas(numero_entero)
def formulario1(buffer, info_estu):
    # Datod de la base de datos
    nombre = info_estu[0]
    carnet = info_estu[1] 
    extension = info_estu[2] 
    tutor = info_estu[3] 
    docente = info_estu[4] 
    titulo = info_estu[5] 
    mencion = info_estu[6]
    # =============================================
    check = 'Si'

    pdf = FPDF(format="letter")
    pdf.add_page()
    pdf.set_font("Times", size=11)

    # Fecha
    def fecha_right():
        meses = ("enero", "febrero", "marzo", "abri", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        hoy = date.today()
        dia = hoy.day.__str__()
        mes = meses[hoy.month - 1]
        year = hoy.year.__str__()
        return dia, mes, year
    fecha = fecha_right()
    dia = fecha[0]
    mes = fecha[1]
    year = fecha[2]

# Modalidad
    pdf.set_xy(89,65)
    pdf.cell(txt=check, ln=1, align="J")

# Postulantes
    pdf.set_xy(32,85)
    pdf.cell(txt=nombre, ln=1, align="J")

    pdf.set_xy(130,85)
    pdf.cell(txt=carnet + ' ' + extension, ln=1, align="J")

# Tutor
    pdf.set_xy(32,128)
    pdf.cell(txt=tutor, ln=1, align="J")

# Titulo
    pdf.set_xy(32,148)
    pdf.multi_cell(150, 11, txt=titulo, ln=1, align="C")

# Fecha
    pdf.set_xy(119,224)
    pdf.cell(txt=dia, ln=1, align="J")
    pdf.set_xy(140,224)
    pdf.cell(txt=mes, ln=1, align="J")
    pdf.set_xy(170,224)
    pdf.cell(txt=year, ln=1, align="J")

# Docente - mencion 
    pdf.set_xy(29,236)
    pdf.cell(txt=docente, ln=1, align="J")
    pdf.set_xy(50,245.8)
    pdf.cell(txt=mencion, ln=1, align="J")
    pdf.output("form1_solapa.pdf")

    input_file = MEDIA_ROOT + "formularios/form1.pdf"  
    watermark_file = "form1_solapa.pdf"
    output_file = "form1_final.pdf"  

    with open(input_file, "rb") as filehandle_input:  
        # read content of the original file
        pdf = PyPDF2.PdfFileReader(filehandle_input)

        with open(watermark_file, "rb") as filehandle_watermark:
            # read content of the watermark
            watermark = PyPDF2.PdfFileReader(filehandle_watermark)

            # get first page of the original PDF
            first_page = pdf.getPage(0)

            # get first page of the watermark PDF
            first_page_watermark = watermark.getPage(0)

            # merge the two pages
            first_page.mergePage(first_page_watermark)

            # create a pdf writer object for the output file
            pdf_writer = PyPDF2.PdfFileWriter()

            # add page
            pdf_writer.addPage(first_page)
            
            # clave para aplicar buffer
            pdf_writer.write(buffer)

    # eliminando el pdf auxiliar
    remove('form1_solapa.pdf')

def formulario2(buffer, info_estu):
    ## info de base de datos
    postulante = info_estu[0]
    asesor = info_estu[1]
    docente_etn1040 = info_estu[2]
    titulo = info_estu[3]
    mencion = info_estu[4]
    abstract= info_estu[5]
    dia = info_estu[6].day.__str__()
    mes = info_estu[6].month.__str__()
    year = info_estu[6].year.__str__()
    fecha_aprobacion = dia+'/'+mes+'/'+year
    if int(mes) <= 6:
        periodo = 'I'
    else:
        periodo = 'II'
    gestion = periodo + '/' + year

    pdf = FPDF(format="letter")
    pdf.add_page()
    pdf.set_font("Times", size=12)

# Postulante
    pdf.set_xy(60,41)
    pdf.cell(w=65, h=8, txt=postulante, ln=1, border=1, align='C')

# Fecha de aprobacion
    pdf.set_xy(167,41)
    pdf.cell(w=23, h=8, txt=fecha_aprobacion, ln=1, border=1, align='C')

# Titulo del tema
    pdf.set_xy(60,55)
    pdf.multi_cell(w=130, h=6, txt=titulo, ln=1, border=1, 
        align='C', max_line_height=10)

# Mencion
    pdf.set_xy(60,77)
    pdf.cell(w=50, h=8, txt=mencion, ln=1, border=1, align='C')

# Gestion academica
    pdf.set_xy(150,77)
    pdf.cell(w=40, h=8, txt=gestion, ln=1, border=1, align='C')

# Asesor
    pdf.set_xy(60,92)
    pdf.cell(w=76, h=8, txt=asesor, ln=1, border=1, align='C')

# Docente
    pdf.set_xy(60,107)
    pdf.cell(w=76, h=8, txt='Ing. '+docente_etn1040, ln=1, border=1, align='C')
# Abstract
    pdf.set_xy(27,133)
    pdf.multi_cell(w=162, h=5, txt=abstract, ln=1, border=0, 
        align='J', max_line_height=150)
# Guardar archivo
    pdf.output("form2_solapa.pdf")

    input_file = MEDIA_ROOT + "formularios/form2.pdf"  
    watermark_file = "form2_solapa.pdf"
    output_file = "form2_final.pdf"  

    with open(input_file, "rb") as filehandle_input:  
        # read content of the original file
        pdf = PyPDF2.PdfFileReader(filehandle_input)

        with open(watermark_file, "rb") as filehandle_watermark:
            # read content of the watermark
            watermark = PyPDF2.PdfFileReader(filehandle_watermark)

            # get first page of the original PDF
            first_page = pdf.getPage(0)

            # get first page of the watermark PDF
            first_page_watermark = watermark.getPage(0)

            # merge the two pages
            first_page.mergePage(first_page_watermark)

            # create a pdf writer object for the output file
            pdf_writer = PyPDF2.PdfFileWriter()

            # add page
            pdf_writer.addPage(first_page)

            pdf_writer.write(buffer)

    # eliminando el pdf auxiliar
    remove('form2_solapa.pdf')

def formulario3(buffer, estudiante, proyecto):
    # mencion
    tele= ''
    control = ''
    sistemas = ''
    if estudiante.mencion == 'Control':
        control = 'V'
    elif estudiante.mencion == 'Sistemas de Computación':
        sistemas = 'V'
    else:
        tele = 'V'
    nombre = estudiante.__str__()
    carnet = estudiante.carnet
    titulo = proyecto.titulo
    docente_tutor = estudiante.tutor.__str__()
    mencion = estudiante.mencion
    empresa = 'Carrera de Ingeniería Electrónica'
    supervisor = 'Ing. Vladimir Barra Garcia'
    cargo = 'Jefe de Carrera Ingeniería Electrónica'
    # individual o multiple
    individual = 'V'
    multiple = ''
    # fecha aprobacion
    fecha_aprobacion = proyecto.fecha_creacion.date().__str__()
    mes = proyecto.fecha_creacion.month.__str__()
    year= proyecto.fecha_creacion.year.__str__()
    # gestion
    if int(mes) <= 6:
        periodo = 'I'
    else:
        periodo = 'II'
    gestion = periodo + '/' + year
    a = '7'
    b = '5'
    c = '20'
    d = '2'
    suma = '34'
    nota_40 = suma
    literal_40 = 'Treita y cuatro'
    nota_60 = '49'
    literal_60 = 'Cuarenta y nueve'
    fecha_cierre = ['8', '08', '2021']
    gestion_cierre = 'II/2021'
    docente_etn1040 = 'Ing. Jorge Mario León Gómez'
    director = 'Ing. Juan Carlos Machicao Aparicio'
# Generacion del pdf
    pdf = FPDF(format="letter")
    pdf.add_page()
    pdf.set_font("Times", size=10)

# Modalidad:
    pdf.set_xy(88,42)
    pdf.cell(w=5, h=6, txt=individual, ln=1, border=1, align='C')

    pdf.set_xy(110,42)
    pdf.cell(w=5, h=6, txt=multiple, ln=1, border=1, align='C')

# Mencion
    pdf.set_xy(150,42)
    pdf.cell(w=5, h=6, txt=tele, ln=1, border=1, align='C')

    pdf.set_xy(162,42)
    pdf.cell(w=5, h=6, txt=control, ln=1, border=1, align='C')

    pdf.set_xy(173,42)
    pdf.cell(w=5, h=6, txt=sistemas, ln=1, border=1, align='C')

# Postulante
    pdf.set_xy(47,48)
    pdf.cell(w=55, h=6, txt=nombre, ln=1, border=0, align='L')

    pdf.set_xy(112,48)
    pdf.cell(w=55, h=6, txt=carnet, ln=1, border=0, align='L')

# Titulo del tema
    pdf.set_xy(54,54.7)
    pdf.multi_cell(w=135, h=4, txt=titulo, ln=1, border=0, 
        align='J', max_line_height=20)

# Docente Tutor
    pdf.set_xy(65,74)
    pdf.cell(w=55, h=6, txt=docente_tutor, ln=1, border=0, align='L')

# Empresa o institucion
    pdf.set_xy(67,90)
    pdf.cell(w=120, h=6, txt=empresa, ln=1, border=0, align='L')

# Supervisor
    pdf.set_xy(50,98)
    pdf.cell(w=45, h=6, txt=supervisor, ln=1, border=0, align='L')

    pdf.set_xy(110,98)
    pdf.cell(w=45, h=6, txt=cargo, ln=1, border=0, align='L')

# Fecha de aprobacion
    pdf.set_xy(83,107)
    pdf.cell(w=20, h=6, txt=fecha_aprobacion, ln=1, border=1, align='C')

    pdf.set_xy(140,107)
    pdf.cell(w=20, h=6, txt=gestion, ln=1, border=0, align='C')

# Notas
    pdf.set_xy(40,139)
    pdf.cell(w=6, h=6, txt=a, ln=1, border=1, align='C')

    pdf.set_xy(72,139)
    pdf.cell(w=6, h=6, txt=b, ln=1, border=1, align='C')

    pdf.set_xy(105,139)
    pdf.cell(w=6, h=6, txt=c, ln=1, border=1, align='C')

    pdf.set_xy(137,139)
    pdf.cell(w=6, h=6, txt=d, ln=1, border=1, align='C')

    pdf.set_xy(170,139)
    pdf.cell(w=6, h=6, txt=suma, ln=1, border=1, align='C')

# Nota de elaboracion del proyecto s/40
    pdf.set_xy(99,147)
    pdf.cell(w=20, h=6, txt=nota_40, ln=1, border=0, align='C')

    pdf.set_xy(127,147)
    pdf.cell(w=60, h=6, txt=literal_40, ln=1, border=0, align='C')

# Trabajo final y defensa publica s/60
    pdf.set_xy(60,169)
    pdf.cell(w=20, h=6, txt=nota_60, ln=1, border=0, align='C')

    pdf.set_xy(92,169)
    pdf.cell(w=80, h=6, txt=literal_60, ln=1, border=0, align='C')

# Trabajo final y defensa publica s/60
    pdf.set_xy(50,212)
    pdf.cell(w=20, h=6, txt=nota_60, ln=1, border=0, align='C')

    pdf.set_xy(75,212)
    pdf.cell(w=80, h=6, txt=literal_60, ln=1, border=0, align='C')

# Fecha de Cierre
    pdf.set_xy(60,224)
    pdf.cell(w=10,h=6, txt=fecha_cierre[0], ln=1, border=0, align='C')

    pdf.set_xy(72,224)
    pdf.cell(w=10,h=6, txt=fecha_cierre[1], ln=1, border=0, align='C')

    pdf.set_xy(85,224)
    pdf.cell(w=11,h=6, txt=fecha_cierre[2], ln=1, border=0, align='C')

# Gestion
    pdf.set_xy(110,224)
    pdf.cell(w=20,h=6, txt=gestion_cierre, ln=1, border=0, align='C')

# Firmas
    pdf.set_xy(35,253)
    pdf.cell(w=70,h=6, txt=docente_etn1040, ln=1, border=0, align='C')
    pdf.set_xy(115,253)
    pdf.cell(w=70,h=6, txt=director, ln=1, border=0, align='C')

# Guardar archivo
    pdf.output("form3_solapa.pdf")
    input_file = MEDIA_ROOT + "formularios/form3.pdf"  
    watermark_file = "form3_solapa.pdf"
    output_file = "form3_final.pdf"  

    with open(input_file, "rb") as filehandle_input:  
        # read content of the original file
        pdf = PyPDF2.PdfFileReader(filehandle_input)

        with open(watermark_file, "rb") as filehandle_watermark:
            # read content of the watermark
            watermark = PyPDF2.PdfFileReader(filehandle_watermark)

            # get first page of the original PDF
            first_page = pdf.getPage(0)

            # get first page of the watermark PDF
            first_page_watermark = watermark.getPage(0)

            # merge the two pages
            first_page.mergePage(first_page_watermark)

            # create a pdf writer object for the output file
            pdf_writer = PyPDF2.PdfFileWriter()

            # add page
            pdf_writer.addPage(first_page)
            pdf_writer.write(buffer)

    # eliminando el pdf auxiliar
    remove('form3_solapa.pdf')


def formulario4(buffer, estudiante, proyecto):
    individual = 'V'
    equipo_de = '1'
    nombre = estudiante.__str__()
    carnet = estudiante.carnet
    extension = 'L.P.'
    tutor = estudiante.tutor.__str__()
    titulo = proyecto.titulo
    nota_40 = proyecto.calificacion.__str__()
    # literal_40 = 'Cuarenta y nueve'
    literal_40 = numero_letra(nota_40)
    fecha = fecha_right()
    # fecha = ['8', 'agosto', '2021']
    docente_etn1040 = 'Jorge Mario León Gómez'

# Generacion del pdf
    pdf = FPDF(format="letter")
    pdf.add_page()
    pdf.set_font("Times", size=12)

# Modalidad:
    pdf.set_xy(88,54)
    pdf.cell(w=5, h=6, txt=individual, ln=1, border=0, align='C')

    pdf.set_xy(140,54)
    pdf.cell(w=5, h=6, txt=equipo_de, ln=1, border=0, align='C')

# Postulante
    pdf.set_xy(35,72)
    pdf.cell(w=100, h=6, txt=nombre, ln=1, border=0, align='L')

    pdf.set_xy(135,72)
    pdf.cell(w=50, h=6, txt=carnet + ' ' + extension, ln=1, border=0, align='L')

# Docente Tutor
    pdf.set_xy(35,98)
    pdf.cell(w=100, h=6, txt='Ing. '+tutor, ln=1, border=0, align='L')

# Titulo del tema
    pdf.set_xy(35,114)
    pdf.multi_cell(w=140, h=8.3, txt=titulo, ln=1, border=0, 
        align='J', max_line_height=60)

# Calificacion obtenida s/40
    pdf.set_xy(50,165)
    pdf.cell(w=15, h=6, txt=nota_40, ln=1, border=0, align='C')

    pdf.set_xy(120,165)
    pdf.cell(w=40, h=6, txt=literal_40, ln=1, border=0, align='C')

# Fecha de Cierre
    pdf.set_xy(109,209)
    pdf.cell(w=10,h=6, txt=fecha[0], ln=1, border=0, align='C')

    pdf.set_xy(130,209)
    pdf.cell(w=20,h=6, txt=fecha[1], ln=1, border=0, align='C')

    pdf.set_xy(168,209)
    pdf.cell(w=15,h=6, txt=fecha[2], ln=1, border=0, align='C')

# Ing. (supongo docente 1040)
    pdf.set_xy(37,234)
    pdf.cell(w=100, h=6, txt=docente_etn1040, ln=1, border=0, align='L')

# Guardar archivo
    pdf.output("form4_solapa.pdf")

    input_file = MEDIA_ROOT + "formularios/form4.pdf"  
    watermark_file = "form4_solapa.pdf"
    output_file = "form4_final.pdf"  

    with open(input_file, "rb") as filehandle_input:  
        # read content of the original file
        pdf = PyPDF2.PdfFileReader(filehandle_input)

        with open(watermark_file, "rb") as filehandle_watermark:
            # read content of the watermark
            watermark = PyPDF2.PdfFileReader(filehandle_watermark)

            # get first page of the original PDF
            first_page = pdf.getPage(0)

            # get first page of the watermark PDF
            first_page_watermark = watermark.getPage(0)

            # merge the two pages
            first_page.mergePage(first_page_watermark)

            # create a pdf writer object for the output file
            pdf_writer = PyPDF2.PdfFileWriter()

            # add page
            pdf_writer.addPage(first_page)

            # buffer
            pdf_writer.write(buffer)

    # eliminando el pdf auxiliar
    remove('form4_solapa.pdf')

