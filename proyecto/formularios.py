#!/usr/bin/env python3 
from fpdf import FPDF
from os import remove
from datetime import date
import PyPDF2
from etn1040_1.settings import MEDIA_ROOT
def formulario1(buffer, info_estu):
    # =============================================
    # Datod de la base de datos
    # check = 'Si'
    # nombre = 'Julio Cesar Cori Ochoa'
    # carnet = 'C.I.: 6002358 L.P.'
    # tutor = 'Ing. Freddy Valle'
    # titulo = 'Diseño de un Sistema de Comparación de Trabajos de Grado \
    # de la Carrera de Ingeniería Electrónica, aplicado a la asignatura \
    # ETN-1040 Proyecto de Grado'
    # dia = '23'
    # mes = 'mayo' 
    # year = '2021'
    # docente = 'Ing. Jorge Mario León Gómez'
    # mencion = 'Sistemas de Computación'
    # =============================================

    # =============================================
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
    pdf.cell(txt=carnet, ln=1, align="J")

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

    # input_file = "../media/formularios/form1.pdf"  
    # input_file = "/home/jcsar/Documents/codesArchLab/programas/Python/webPython/djangoPython/etn1040_1/media/formularios/form1.pdf"  
    print(MEDIA_ROOT)
    input_file = MEDIA_ROOT + "formularios/form1.pdf"  
    watermark_file = "form1_solapa.pdf"
    output_file = "form1_final.pdf"  
    # output_file = buffer

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

            # with open(output_file, "wb") as filehandle_output:
                # # write the watermarked file to the new file
                # pdf_writer.write(filehandle_output)

    # eliminando el pdf auxiliar
    remove('form1_solapa.pdf')
