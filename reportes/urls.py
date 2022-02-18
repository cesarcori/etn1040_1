from django.urls import path

from . import views

app_name = 'reportes'

urlpatterns = [
    path('carta-tutor-acepto/<int:pk>', views.cartaTutorAcepto, name='carta-tutor-acepto'),
    path('formulario-aceptacion/<int:id_est>', views.formAceptacion, name='form-aceptacion'),
]


