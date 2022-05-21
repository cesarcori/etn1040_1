from django.urls import path

from .views import *

app_name = 'documentos'

urlpatterns = [
    path('', verDocumento, name='ver_documento'),
    path('subir/<str:tipo>/<int:pk>', subirDocumento, name='subir_documento'),
    path('ver/<int:pk>/<str:tipo>', verDocumento, name='ver_documento'),
]
