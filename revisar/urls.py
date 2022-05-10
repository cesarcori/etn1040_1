from django.urls import path

from . import views

app_name = 'revisar'

urlpatterns = [
    path('<str:documento>&<int:id_revisor>/', views.revisarDocumento, name='revisar_documento'),
    path('<str:documento>&<int:id_revisor>/<int:id_sala_doc>/', views.crearSalaRevisar, name='crear_sala_revisar'),
    path('<int:id_sala_rev>/mensajes/', views.mensajes, name='mensajes'),
    path('caramba/', views.mensajes, name='crear_mensaje'),
    path('dar-vistoBueno/<int:id_sala_doc>', views.darVistoBueno, name='dar_visto_bueno'),
    path('calificar-sala/<int:pk>', views.calificarSalaRevision, name='calificar_sala'),
    path('calificar-serminario/<int:pk>/', views.calificarSeminario, name='calificar_seminario'),
    path('calificar-cronograma/<int:pk>/', views.calificarCronograma, name='calificar_cronograma'),
    path('registrar-participacion-serminario/<int:pk>/', views.registrarParticipacionSeminario, name='registrar_seminario'),
    path('registrar-cumplimiento-cronograma/<int:pk>/', views.registrarCumplimientoCronograma, name='registrar_cronograma'),
]
