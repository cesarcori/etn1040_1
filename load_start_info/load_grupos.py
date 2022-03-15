#!/usr/bin/env python3 
from django.contrib.auth.models import Group
# para ejecutar este script dentro de shell ejecutar el siguiente comando en
# la terminal, dentro del proyecto.
# python manage.py shell -i python < load_db.py
# otra forma de poblar datos es mediante dumpdata y fixtures
if not Group.objects.all().count() == 7:
    grupos = ['docente','administrador',
            'tutor','tribunal','estudiante',
            'director','solicitud']
    for grupo in grupos:
        Group.objects.get_or_create(name=grupo)
else:
    print("*** Ya se cargo los grupos")
    


