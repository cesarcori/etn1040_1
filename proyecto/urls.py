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
    path('progreso-est/<int:pk_est>', views.progresoEstudiante, name='progreso_estudiante'),
    path('info-solicitante/<int:pk_sol>', views.enlaceSolicitante,
        name='enlace_solicitante'),
    path('info-doc/<int:pk_doc>/', views.enlaceDocente, name='enlace_docente'),
    path('info-tut/<int:pk_tutor>/', views.enlaceTutor, name='enlace_tutor'),
    path('lista_est/', views.listaEstudiantes, name='lista_estudiantes'),
    path('lista_doc/', views.listaDocentes, name='lista_docentes'),
    path('lista_tut/', views.listaTutores, name='lista_tutores'),

    path('agregar-doc/', views.agregarDocente, name='agregar_docente'),

    
    path('paso1/', views.paso1, name='paso1'),
    path('paso2/', views.paso2, name='paso2'),
    path('paso3/', views.paso3, name='paso3'),
    path('paso4/', views.paso4, name='paso4'),
    path('paso4/entrega-perfil', views.entregaPerfil, name='entrega_perfil'),
    path('paso4/entrega-perfil/crear-sala-revisar', views.crearSalaRevisar,
        name='crear_sala'),
    # path('paso4/entrega-perfil/sala/<int:pk_sala>/', views.salaRevisar,
        # name='sala_revisar'),
    path('sala-rev/<int:pk_sala>/',views.salaRevisar,name='sala_revisar'),
    path('sala-rev/doc/<int:pk_sala>/',views.salaRevisarEstDoc,
        name='sala_revisar_est_doc'),
    path('sala-rev/tut/<int:pk_sala>/',views.salaRevisarEstTut,
        name='sala_revisar_est_tut'),
    # path('paso4/pdf/', views.some_view, name='some_view'),
    path('paso4/carta-aceptacion/', views.carta_aceptacion_tutor,
        name='carta_aceptacion_tutor'),
    path('paso4/carta-solicitud/', views.carta_solicitud_tutor,
        name='carta_solicitud_tutor'),
    path('paso5/', views.paso5, name='paso5'),
    path('paso6/', views.paso6, name='paso6'),
    
    path('material-para-est/', views.materialParaEst, name='material_para_estudiante'),

    path('error/', views.error , name='error_pagina'),
    
]
