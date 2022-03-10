from django.urls import path

from . import views

app_name = 'mensaje'

urlpatterns = [
    path('', views.index, name='index'),
    path('par/', views.par, name='enviar_mensaje_par'),
]


