#!/usr/bin/env python3 
from django.contrib.auth.models import Group
# para ejecutar este script dentro de shell ejecutar el siguiente comando en
# la terminal, dentro del proyecto.
# python manage.py shell -i python < load_db.py
# otra forma de poblar datos es mediante dumpdata y fixtures
grupos = ['docente','administrador',
        'tutor','tribunal','estudiante',
        'director','solicitud']
for grupo in grupos:
    Group.objects.get_or_create(name=grupo)
f= open("load_start_info/grupos_creado.txt","w+")
f.write("Se cargo los grupos con exito.")
f.close
    


