from django.urls import path

from . import views

app_name = 'reportes'

urlpatterns = [
    path('indicaciones-tutor/<int:pk>', views.reporteIndicacionesTutor, name='indicaciones_tutor'),
    path('carta-tutor-acepto/<int:pk>', views.cartaTutorAcepto, name='carta-tutor-acepto'),
    path('formulario-aceptacion/<int:pk>', views.formularioAceptacion, name='formulario-aceptacion'),
]


