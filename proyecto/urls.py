from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('', views.home, name='home'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('registro/', views.registerPage, name="registro"),

    path('docente/', views.docente, name='docente'),
    path('tutor/', views.tutor, name='tutor'),
    path('estudiante/', views.estudiante, name='estudiante'),

    path('perfil/', views.perfilUsuarios, name='perfil'),
    path('busqueda/', views.busquedaProyectos, name='busqueda'),
    path('comp-todos/', views.compartirTodos, name='compartir_con_todos'),
    path('comp-personal/', views.compartirPersonal, name='compartir_personal'),

    path('info-est/', views.enlaceEstudiante, name='enlace_estudiante'),
    path('info-doc/', views.enlaceDocente, name='enlace_docente'),
    path('lista_est/', views.listaEstudiantes, name='lista_estudiantes'),
    path('lista_doc/', views.listaDocentes, name='lista_docentes'),
    #path('registro-est/', views.registroEstudiante, name='registro_estudiante'),

]
