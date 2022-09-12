#!/usr/bin/env python3 
from actividades.models import *
import csv
# para ejecutar este script dentro de shell ejecutar el siguiente comando en
# la terminal, dentro del proyecto.
# python manage.py shell -i python < load_db.py
# otra forma de poblar datos es mediante dumpdata y fixtures
if not Actividad.objects.all().count() > 25:
    with open('load_start_info/actividades.csv', 'r') as f:
        reader = csv.DictReader(f)
        items = list(reader)
        # items = items[0:5]

    for item in items:
        nombre = item.get('nombre'),
        detalle = item.get('detalle'),
        valor = item.get('valor'),
        orden = item.get('orden')
        nombre_humano = item.get('nombre_humano')
        print(f"Cargando actividad: {nombre[0]}")
        # print(nombre[0], detalle[0], valor[0], orden)
        Actividad.objects.create(
            nombre=nombre[0],
            detalle=detalle[0],
            valor=valor[0],
            orden=orden,
            nombre_humano=nombre_humano[0],
            )
else:
    print("*** Ya se cargo las actividades")
# f= open("load_start_info/actividades_creado.txt","w+")
# f.write("Se cargo las actividades con exito")
# f.close
    


