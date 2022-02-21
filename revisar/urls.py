from django.urls import path

from . import views

app_name = 'revisar'

urlpatterns = [
    path('<str:documento>&<int:id_revisor>/', views.revisarDocumento, name='revisar_documento'),
    path('<str:documento>&<int:id_revisor>/<int:id_sala_doc>/', views.crearSalaRevisar, name='crear_sala_revisar'),
    path('<int:id_sala_rev>/mensajes/', views.mensajes, name='mensajes'),
    path('caramba/', views.mensajes, name='crear_mensaje'),
    path('dar-vistoBueno/<int:id_sala_doc>', views.darVistoBueno, name='dar_visto_bueno'),
]


