from django.urls import path

from .views import *

app_name = 'tiempos'

urlpatterns = [
    path('<int:pk>', resumen, name='resumen'),
]
