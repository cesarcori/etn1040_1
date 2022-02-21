from django.urls import path

from . import views

app_name = 'reportes'

urlpatterns = [
    path('indicaciones-tutor/<int:pk>', views.reporteIndicacionesTutor, name='indicaciones_tutor'),
    path('carta-tutor-acepto/<int:pk>', views.cartaTutorAcepto, name='carta-tutor-acepto'),
    path('formulario-aceptacion/<int:pk>', views.formularioAceptacion, name='formulario-aceptacion'),
    path('capitulos-tutor/<int:pk>', views.firmaTutorCapitulos, name='capitulos-tutor'),
    path('carta-final/<int:pk>', views.cartaFinal, name='carta_final'),
    path('formulario-solicitud-tribunal/<int:pk>', views.formularioSolicitudTribunal, name='formulario_solicitud_tribunal'),
    path('formulario-registro-seguimiento/<int:pk>', views.formularioRegistroSeguimiento, name='formulario_registro_seguimiento'),
    path('formulario-reg-seg/auspicio/<int:pk>', views.auspicioFormRegSeg, name='auspicio_f3'),
    path('formulario-materia/<int:pk>', views.formularioMateria, name='formulario_materia'),
]


