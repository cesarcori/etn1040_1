from django.contrib import admin
from django.urls import path
# cambia password
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [

    path('', views.home, name='home'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('registro/', views.registerPage, name="registro"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),  

    path('eliminar-usuario/<int:usuario_id>', views.eliminarUsuario, name="eliminar_usuario"),
    path('sorteo-docente/', views.estudiante, name='sorteo_docente'),

    path('docente/', views.docente, name='docente'),
    path('tutor/', views.tutor, name='tutor'),
    path('tribunal/', views.tribunal, name='tribunal'),
    path('director/', views.director, name='director'),
    path('solicitud/', views.solicitud, name='solicitud'),
    path('asignar-tribu/<int:pk>', views.asignarTribunal, name='asignar_tribunal'),
    path('confi-asign-tr/<int:pk_equi>/<int:id_trib>', views.confirmarAsignarTribunal, name='confirmar_asignar_tribunal'),
    path('firmas/', views.firmas, name='firmas'),
    path('firmas/cargar-firma/', views.cargarFirma, name='cargar_firma'),
    path('tutor/solicitud-tutoria/<int:pk>', views.solicitudTutoria, name='solicitud_tutoria'),
    path('estudiante/', views.estudiante, name='estudiante'),

    path('passcontra/', views.editarPassword, name='editar_password'),
    path('resetPass/<int:id_user>', views.resetearPassword, name='resetear_password'),

    path('perfil/', views.perfilUsuarios, name='perfil'),
    path('perfil/editar', views.editarPerfil, name='editar_perfil'),
    # path('busqueda/', views.busquedaProyectos, name='busqueda'),
    # path('busqueda/agregar/', views.agregarProyecto, name='agregar_proyecto'),
    path('mis_comun/', views.misComunicados, name='mis_comunicados'),
    path('mis_comun/eliminar/<int:id_comunicado>', views.eliminarComunicado, name='eliminar_comunicado'),
    path('crear-comun/', views.crearComunicado, name='crear_comunicado'),
    path('mensaje-personal/<int:pk_doc_tut_est>', views.mensajePersonal, name='mensaje_personal'),
    path('comun-doc-est/', views.comunicadosDocEst, name='comunicados_doc_est'),
    path('comun-tut-est/', views.comunicadosTutEst, name='comunicados_tut_est'),
    path('comp-personal/', views.compartirPersonal, name='compartir_personal'),

    path('info-est/<int:pk_est>', views.enlaceEstudiante, name='enlace_estudiante'),
    path('info-est-tit/<int:id_est_tit>', views.enlaceEstudianteTitulado, name='enlace_estudiante_titulado'),
    # path('reporte-est/<int:id_est>', views.reporteEstudiante, name='reporte_estudiante'),
    # path('reporte-est/imprimir/<int:id_est>', views.imprimirReporteEstudiante, name='imprimir_reporte'),
    path('progreso-est/<int:pk>', views.progresoEstudiante, name='progreso_estudiante'),
    # path('progreso-est/vis-bu-per/<int:id_est>', views.vistoBuenoPerfil, name='visto_bueno_perfil'),
    # path('progreso-est/vis-bu-pro/<int:id_est>', views.vistoBuenoProyecto, name='visto_bueno_proyecto'),
    # path('progreso-est/vis-bu-tri/<int:id_est>', views.vistoBuenoTribunal, name='visto_bueno_tribunal'),
    path('progreso-est/crono/<int:pk>', views.ver_cronograma, name='ver_cronograma'),
    path('progreso-est/perfil-corregido/<int:id_sala>', views.perfilCorregido, name='perfil_corregido'),
    path('progreso-est/proyecto-corregido/<int:id_sala>', views.proyectoCorregido, name='proyecto_corregido'),
    path('info-solicitante/<int:pk_sol>', views.enlaceSolicitante,
        name='enlace_solicitante'),
    path('info-doc/<int:pk_doc>/', views.enlaceDocente, name='enlace_docente'),
    path('info-tut/<int:pk_tutor>/', views.enlaceTutor, name='enlace_tutor'),
    path('info-tri/<int:pk_tribunal>/', views.enlaceTribunal, name='enlace_tribunal'),
    path('lista_est/', views.listaEstudiantes, name='lista_estudiantes'),
    path('lista_est_tit/', views.listaEstudianteTitulado, name='lista_estudiante_titulado'),
    path('lista_doc/', views.listaDocentes, name='lista_docentes'),
    path('lista_tut/', views.listaTutores, name='lista_tutores'),
    path('lista_tri/', views.listaTribunales, name='lista_tribunales'),

    path('agregar-doc/', views.agregarDocente, name='agregar_docente'),
    path('agregar-tut/', views.agregarTutor, name='agregar_tutor'),
    path('agregar-tri/', views.agregarTribunal, name='agregar_tribunal'),

    path('paso1/', views.paso1, name='paso1'),
    path('paso1/conf-reg/<int:id_reg>', views.confirmarReglamento, name='confirmar_reglamento'),
    path('paso1/conf-mate/<int:id_mat>', views.confirmarMaterialDocente, name='confirmar_material_docente'),
    path('paso2/', views.paso2, name='paso2'),
    path('paso3/', views.paso3, name='paso3'),
    # path('paso3/reporte-tutor-acepto/<int:id_est>', views.reporteTutorAcepto, name='reporte_tutor_acepto'),
    # path('paso3/indicaciones-tutor/<int:id_est>', views.reporteIndicacionesTutor, name='indicaciones_tutor'),
    path('paso4/', views.paso4, name='paso4'),
    # path('paso4/entrega-perfil', views.entregaPerfil, name='entrega_perfil'),
    # path('paso4/entrega-perfil/crear-sala-revisar', views.crearSalaRevisar, name='crear_sala'),
    # path('sala-rev/<int:pk_sala>/',views.salaRevisar,name='sala_revisar'),
    # path('sala-rev/doc/<int:pk_sala>/',views.salaRevisarEstDoc, name='sala_revisar_est_doc'),
    # path('sala-rev/tut/<int:pk_sala>/',views.salaRevisarEstTut, name='sala_revisar_est_tut'),
    path('paso4/carta-aceptacion/', views.carta_aceptacion_tutor, name='carta_aceptacion_tutor'),
    path('paso4/carta-solicitud/', views.carta_solicitud_tutor, name='carta_solicitud_tutor'),
    path('paso4/registro-perfil/', views.registro_perfil, name='registro_perfil'),
    path('paso4/perfil-registrado/', views.ver_perfil_registrado, name='ver_perfil_registrado'),
    path('cronograma-actividad/', views.cronograma_actividad, name='cronograma_actividad'),
    # path('paso4/formulario-aprobacion/<int:id_est>', views.formulario_1, name='formulario_1'),
    path('paso4/eliminar-actividad/<int:id_act>', views.eliminar_actividad, name='eliminar_actividad'),
    path('paso4/cronograma-actividad/registrar', views.cronograma_registrar, name='cronograma_registrar'),
    path('paso5/', views.paso5, name='paso5'),
    path('paso5/cronograma-control/', views.cronograma_control, name='cronograma_control'),
    # path('plantilla-revision/<int:id_est>', views.reporteCapitulos, name='reporte_capitulos'),
    # path('entrega-proyecto/', views.entregaProyecto, name='entrega_proyecto'),
    # path('entrega-proyecto/crear-sala-revisar-proy', views.crearSalaRevisarProyecto, name='crear_sala_proyecto'),
    # path('sala-rev-proy/<int:pk_sala>/',views.salaRevisarProyecto,name='sala_revisar_proyecto'),
    # path('sala-rev-proy/doc/<int:pk_sala>/',views.salaRevisarProyEstDoc, name='sala_revisar_proy_est_doc'),
    # path('sala-rev-proy/tut/<int:pk_sala>/',views.salaRevisarProyEstTut, name='sala_revisar_proy_est_tut'),
    path('paso5/registro-proyecto/', views.registroProyecto, name='registro_proyecto'),
    path('paso5/proyecto/', views.ver_proyecto_grado, name='ver_proyecto_grado'),

    path('paso6/', views.paso6, name='paso6'),
    path('paso6/solicitud-tribu/int:id_est>', views.solicitudTribunal, name='solicitud_tribunal'),
    # path('paso6/entrega-tribu/<int:id_trib>/<int:id_est>', views.entregaTribunal, name='entrega_tribunal'),
    # path('sala-rev-trib/<int:pk_sala>/',views.salaRevisarTribunal,name='sala_revisar_tribunal'),
    # path('sala-rev/trib/<int:pk_sala>/<int:id_trib>',views.salaRevisarEstTrib, name='sala_revisar_est_trib'),
    # path('entrega-tribu/crear-sala-revisar-trib/<int:id_trib>', views.crearSalaRevisarTribunal, name='crear_sala_tribunal'),
    # path('paso6/carta-final/<int:id_est>', views.carta_final_tutor, name='carta_final'),
    path('paso6/ultimos-formularios/', views.ultimosFormularios, name='ultimos_formularios'),
    # path('paso6/formulario-material-proyecto-grado/<int:id_est>', views.formulario_2, name='formulario_2'),
    # path('paso6/formulario-3/<int:id_est>', views.formulario_3, name='formulario_3'),
    # path('paso6/formulario-3/auspicio/<int:id_est>', views.auspicioF3, name='auspicio_f3'),
    # path('paso6/formulario-4/<int:id_est>', views.formulario_4, name='formulario_4'),
    path('paso6/registro-proyecto-trib/', views.registroProyectoTribunal, name='registro_proyecto_tribunal'),
    path('paso6/proyecto-trib/', views.ver_proyecto_tribunal, name='ver_proyecto_tribunal'),
    path('calificar-proyecto-tri/<int:pk>/', views.calificarProyectoTribunal, name='calificar_proyecto_tribunal'),

    path('calificar-proyecto/<int:pk>/', views.calificarProyecto, name='calificar_proyecto'),
    path('solicitar-tribunal-d/<int:pk>/', views.solicitarTribunalDocente, name='solicitar_tribunal_docente'),
    
    path('material-para-est/', views.materialParaEst, name='material_para_estudiante'),
    path('material-para-est/eliminar/<int:id_material>', views.eliminarMaterialParaEst, name='eliminar_material'),

    # path('confirmar-paso-1/', views.confirmarPaso1, name='confirmar_paso_1'),
    path('confirmar-paso-2/', views.confirmarPaso2, name='confirmar_paso_2'),
    path('confirmar-paso-3/', views.confirmarPaso3, name='confirmar_paso_3'),
    path('confirmar-paso-4/', views.confirmarPaso4, name='confirmar_paso_4'),
    # path('confirmar-paso-5/', views.confirmarPaso5, name='confirmar_paso_5'),
    path('confirmar-paso-6/', views.confirmarPaso6, name='confirmar_paso_6'),

    path('error/', views.error , name='error_pagina'),
    
]
