#!/usr/bin/env python3 
from proyecto.models import Reglamento
# para ejecutar este script dentro de shell ejecutar el siguiente comando en
# la terminal, dentro del proyecto.
# python manage.py shell -i python < load_db.py
# otra forma de poblar datos es mediante dumpdata y fixtures
Reglamento.objects.create(archivo='reglamentos/reglamento1.pdf')    
Reglamento.objects.create(archivo='reglamentos/reglamento2.pdf')    
Reglamento.objects.create(archivo='reglamentos/resolucion1.pdf')    

f= open("load_start_info/reglamentos_creado.txt","w+")
f.write("Se cargo los reglamentos con exito")
f.close
