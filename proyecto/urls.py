from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('', views.bienvenidos, name='bienvenidos'),

    path('docente/', views.docente, name='docente'),
    path('tutor/', views.tutor, name='tutor'),
    path('estudiante/', views.estudiante, name='estudiante'),

    path('perfil/', views.perfilUsuarios, name='perfil'),
    path('busqueda/', views.busquedaProyectos, name='busqueda'),

    

]
