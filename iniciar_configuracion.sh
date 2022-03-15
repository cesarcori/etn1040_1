#!/bin/bash 

# ejecutar el archivo para realizar las configuraciones iniciales

# crear entorno virtual
DIR_VIR="../virtual-django/"
if [ ! -d "$DIR_VIR" ]; then
  # Take action if $DIR not exists. #
    echo "Creando entorno virtual ${DIR_VIR}..."
    virtualenv ../virtual-django
else
    echo "Ya se tiene el entorno virtual"
fi
source ../virtual-django/bin/activate
# Instalar librerias necesarias de python
pip install -r requirements.txt

DIR="media/"
if [ ! -d "$DIR" ]; then
  # Take action if $DIR not exists. #
    echo "Creando entorno virtual ${DIR}..."
    mkdir -p media
    cp -r archivos_defecto/firmas/ media/
    cp -r archivos_defecto/formularios/ media/
    cp -r archivos_defecto/imagenes/ media/
    cp -r archivos_defecto/reglamentos/ media/
else
    echo "Ya se tiene el directorio media"
fi

# nos direccionamos a la carpeta de carga de informacion
#cd load_start_info
python manage.py makemigrations
python manage.py migrate
# Cargar datos de actividades.
#python3 manage.py shell < load_start_info/load_actividades.py

# crear los grupos: docente, tutor, tribunal, estudiante, administrador.
# agregar datos iniciales importantes: administrador, director, 3 docentes por
# mencion.
## Cargar base de datos archivo csv
#python3 manage.py shell < load_proyectos.py
## Cargar reglamentos.
#python3 manage.py shell < load_reglamentos.py


