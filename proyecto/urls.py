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
    path('mis_comun/', views.misComunicados, name='mis_comunicados'),
    path('crear-comun/', views.crearComunicado, name='crear_comunicado'),
    path('mensaje-personal/<int:pk_doc_tut_est>', views.mensajePersonal, name='mensaje_personal'),
    path('comun-doc-est/', views.comunicadosDocEst, name='comunicados_doc_est'),
    path('comun-tut-est/', views.comunicadosTutEst, name='comunicados_tut_est'),
    path('comp-personal/', views.compartirPersonal, name='compartir_personal'),

    path('info-est/<int:pk_est>', views.enlaceEstudiante, name='enlace_estudiante'),
    path('info-solicitante/<int:pk_sol>', views.enlaceSolicitante,
        name='enlace_solicitante'),
    path('info-doc/<int:pk_doc>/', views.enlaceDocente, name='enlace_docente'),
    path('info-tut/<int:pk_tutor>/', views.enlaceTutor, name='enlace_tutor'),
    path('lista_est/', views.listaEstudiantes, name='lista_estudiantes'),
    path('lista_doc/', views.listaDocentes, name='lista_docentes'),

    path('agregar-doc/', views.agregarDocente, name='agregar_docente'),

    
    path('paso1/', views.paso1, name='paso1'),
    path('paso2/', views.paso2, name='paso2'),
    path('paso3/', views.paso3, name='paso3'),
    path('paso4/', views.paso4, name='paso4'),
    path('paso5/', views.paso5, name='paso5'),
    path('paso6/', views.paso6, name='paso6'),
    
    path('error/', views.error , name='error_pagina'),
    
]
