#!/usr/bin/env python3 
# from actividades.models import *
import csv
from datetime import datetime
# para ejecutar este script dentro de shell ejecutar el siguiente comando en
# la terminal, dentro del proyecto.
# python manage.py shell -i python < load_db.py
# otra forma de poblar datos es mediante dumpdata y fixtures
with open('./actividades.csv', 'r') as f:
    reader = csv.DictReader(f)
    items = list(reader)
    # items = items[0:5]

for item in items:
    nombre = item.get('nombre'),
    detalle = item.get('detalle'),
    valor = item.get('valor'),
    orden = item.get('orden')
    print(nombre[0], detalle[0], valor[0], orden)
    # Actividad.objects.create(
        # nombre=nombre[0],
        # detalle=detalle[0],
        # valor=valor[0],
        # orden=orden[0],
        # )
    


