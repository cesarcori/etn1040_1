from busquedas.models import ProyectosExcel
import csv
from datetime import datetime
# para ejecutar este script dentro de shell ejecutar el siguiente comando en
# la terminal, dentro del proyecto.
# python manage.py shell -i python < load_db.py
# otra forma de poblar datos es mediante dumpdata y fixtures
with open('actividades.csv', 'r') as f:
    reader = csv.DictReader(f)
    items = list(reader)
    # items = items[0:5]

for item in items:
    nombre = item.get('nombre'),
    detalle = item.get('detalle'),
    valor = item.get('valor'),
    orden = item.get('orden')
    print(tesistas[0], autor[0], titulo[0])
    Actividad.objects.create(
        nombre=nombre,
        detalle=detalle,
        valor=valor,
        orden=orden,
        )
    


