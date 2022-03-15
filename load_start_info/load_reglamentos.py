#!/usr/bin/env python3 
from proyecto.models import Reglamento
# para ejecutar este script dentro de shell ejecutar el siguiente comando en
# la terminal, dentro del proyecto.
# python manage.py shell -i python < load_db.py
# otra forma de poblar datos es mediante dumpdata y fixtures
if not Reglamento.objects.all().count() == 3:
    Reglamento.objects.create(archivo='reglamentos/reglamento1.pdf')    
    Reglamento.objects.create(archivo='reglamentos/reglamento2.pdf')    
    Reglamento.objects.create(archivo='reglamentos/resolucion1.pdf')    
else:
    print("*** Ya se cargo los reglamentos")
