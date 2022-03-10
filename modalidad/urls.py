from django.urls import path

from . import views

app_name = 'modalidad'

urlpatterns = [
    path('individual/', views.individual, name='individual'),
    path('multiple/', views.multiple, name='multiple'),
    path('solicitud/', views.solicitud, name='solicitud'),
    path('ver-solicitud/<int:id_obj>', views.verSolicitud, name='ver_solicitud'),
    path('rechazar-solicitud/<int:id_obj>', views.rechazarSolicitud, name='rechazar_solicitud'),
    path('ver-rechazo/<int:id_obj>', views.verRechazo, name='ver_rechazo'),
    path('aprobar-solicitud/<int:id_obj>', views.aprobarSolicitud, name='aprobar_solicitud'),
    path('solicitud-invitado/', views.verSolicitudInvitado, name='ver_solicitudes_invitado'),
    path('aprobar-solicitud-inv/<int:pk>', views.aprobarSolicitudInvitado, name='aprobar_solicitud_invitado'),
    path('rechazar-solicitud-inv/<int:pk>', views.rechazarSolicitudInvitado, name='rechazar_solicitud_invitado'),
    path('modificar-nombre/', views.modificarNombreEquipo, name='modificar_nombre_equipo'),
    path('agregar-integrantes/', views.agregarIntegrantes, name='agregar_integrantes'),
    path('ver-equipo/<int:pk>', views.verEquipo, name='ver_equipo'),
]


