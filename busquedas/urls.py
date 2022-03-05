from django.urls import path

from .views import *

app_name = 'busquedas'

urlpatterns = [
    path('proyectos/', buscarProyectos, name='buscar_proyectos'),
    path('datos/', buscarPorDatos, name='buscar_datos'),
    path('datos-ex/', buscarDatosProyectosExcel, name='buscar_excel'),
    path('agregar-proy/', agregarProyecto, name='agregar_proyecto'),
    path('ver-proy/', verProyectos, name='ver_proyectos'),
]
