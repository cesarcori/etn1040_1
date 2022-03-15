#!/usr/bin/env python3 
from proyecto.models import Mencion
# para ejecutar este script dentro de shell ejecutar el siguiente comando en
# la terminal, dentro del proyecto.
# python manage.py shell -i python < load_db.py
# otra forma de poblar datos es mediante dumpdata y fixtures
if not Mencion.objects.all().count() >= 3:
    menciones = ['Sistemas de Computación','Telecomunicación','Control']
    for mencion in menciones:
        Mencion.objects.create(nombre=mencion)
else:
    print("*** Ya se cargo las menciones")



