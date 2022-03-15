#!/usr/bin/env python3 
from busquedas.models import ProyectosExcel
import csv
from datetime import datetime
# para ejecutar este script dentro de shell ejecutar el siguiente comando en
# la terminal, dentro del proyecto.
# python manage.py shell -i python < load_db.py
# otra forma de poblar datos es mediante dumpdata y fixtures
with open('load_start_info/proyectos_normalizados.csv', 'r') as f:
    reader = csv.DictReader(f)
    items = list(reader)

for item in items:
    sigla_id = item.get('ID'),
    tesistas = int(item.get('TESISTAS')),
    autor = item.get('AUTOR'),
    titulo = item.get('TITULO'),
    tutor = item.get('TUTOR')
    docente = item.get('DOCENTE-1040')
    mencion = item.get('MENCION')
    fecha = item.get('FECHA')
    print(f"Proyecto: {titulo[0]}")
    # print(sigla_id[0], tesistas[0], autor[0], titulo[0], tutor, docente, mencion, fecha)
    ProyectosExcel.objects.create(
        tesistas = tesistas[0],
        sigla_id = sigla_id[0],
        autor = autor[0],
        titulo = titulo[0],
        tutor = tutor,
        docente = docente,
        mencion = mencion,
        fecha_concluida = datetime.strptime(fecha, "%Y-%m-%d"),
        )
f= open("load_start_info/proyectos_creado.txt","w+")
f.write("Se cargo los proyectos con exito")
f.close


