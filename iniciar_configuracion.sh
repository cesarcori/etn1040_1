#!/bin/bash 

# ejecutar el archivo para realizar las configuraciones iniciales

# installar entorno virtual virtualenv

pip3 install virtualenv

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
pip3 install -r requirements.txt

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

# creando la base de datos
python3 manage.py makemigrations
python3 manage.py migrate

# Cargar datos de actividades.
python3 manage.py shell < load_start_info/load_actividades.py

# Cargar base de datos archivo proyectos csv
python3 manage.py shell < load_start_info/load_proyectos_csv.py

## Cargar reglamentos.
python3 manage.py shell < load_start_info/load_reglamentos.py

# crear los grupos: docente, tutor, tribunal, estudiante, administrador.
python3 manage.py shell < load_start_info/load_grupos.py

# agregar datos iniciales importantes: administrador, director, 3 docentes por
python3 manage.py shell < load_start_info/load_usuarios.py

# agregar menciones.
python3 manage.py shell < load_start_info/load_menciones.py


