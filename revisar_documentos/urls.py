from django.urls import path

from . import views

app_name = 'revisar_documentos'

urlpatterns = [
    path('revisiones/<int:pk>/', views.revisiones, name='revisiones'),
    path('configurar/<int:pk>/', views.configurar, name='configurar'),
    path('configurar/cambiar/<int:pk>/', views.cambiarPredeterminado, name='cambiar_predeterminado'),
    path('crear/sala/personal/<int:pk>/', views.crearSalaPersonal, name='crear_sala_personal'),
    path('modificar/sala/personal/<int:pk>/<int:pk_equipo>/', views.modificarSalaPersonal, name='modificar_sala_personal'),
    path('eliminar/sala/personal/<int:pk>/<int:pk_equipo>/', views.eliminarSalaPersonal, name='eliminar_sala_personal'),
    path('estudi/<str:documento>&<int:id_revisor>/', views.revisarDocumentoEstudiante, name='revisar_documento_estudiante'),
    path('revisor/<str:documento>&<int:id_equipo>/', views.revisarDocumentoRevisor, name='revisar_documento_revisor'),
    path('crear/<str:documento>/<int:id_sala_doc>/', views.crearSalaRevisar, name='crear_sala_revisar'),
    path('crear/sala/<str:documento>/<int:id_sala_doc>/', views.crearSalaSinNota, name='crear_sala_sin_nota'),
    path('eliminar/sala/<int:id_sala_rev>/', views.eliminarSalaRevisar, name='eliminar_sala_revisar'),
    path('cerrar/sala/<int:id_sala_rev>/', views.cerrarSalaRevisar, name='cerrar_sala_revisar'),
    path('subir/documento/<int:pk>/', views.subirDocumento, name='subir_documento'),
    path('mensajes/<int:id_sala_rev>/', views.mensajes, name='mensajes'),
    path('dar-vistoBueno/<int:id_sala_doc>', views.darVistoBueno, name='dar_visto_bueno'),
    path('registrar-documento/<int:id_sala_doc>', views.registrarDocumento, name='registrar_documento'),
    path('calificar-sala/<int:pk>', views.calificarSalaRevision, name='calificar_sala'),
    path('modificar/nota_max/<int:id_sala>', views.modificarNotaMax, name='modificar_nota_max'),
    path('calificar-serminario/<int:pk>/', views.calificarSeminario, name='calificar_seminario'),
    path('calificar-cronograma/<int:pk>/', views.calificarCronograma, name='calificar_cronograma'),
    path('registrar-participacion-serminario/<int:pk>/', views.registrarParticipacionSeminario, name='registrar_seminario'),
    path('registrar-cumplimiento-cronograma/<int:pk>/', views.registrarCumplimientoCronograma, name='registrar_cronograma'),
]
