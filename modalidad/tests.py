from django.test import TestCase

from django.utils import timezone

from .models import *

class SolicitudTest(TestCase):
            
    def test_solicitud(self):
        w = Solicitud.objects.create(
            asunto = 'Solicitud de Modalidad Múltiple',
            detalle = """El tutor me sugiere que el proyecto lo elaboren 2 personas.""",
            visto = False,
            aprobar = True,
            fecha_creacion = timezone.now()
        )

        self.assertTrue(isinstance(w, Solicitud))

class RechazarSolicitudTest(TestCase):
            
    def test_rechazar_solicitud(self):
        w = RechazarSolicitud.objects.create(
            asunto = 'Solicitud de Modalidad Múltiple',
            detalle = """El tutor me sugiere que el proyecto lo elaboren 2 personas.""",
            visto = False,
            fecha_creacion = timezone.now()
        )

        self.assertTrue(isinstance(w, RechazarSolicitud))

class SolicitudIntegranteTest(TestCase):
            
    def test_solicitud_integrante(self):
        w = SolicitudIntegrante.objects.create(
            correo_invitado = "ejemplo@gmail.com",
            visto = False,
            estado = "aprobar",
            fecha_creacion = timezone.now()
        )

        self.assertTrue(isinstance(w, SolicitudIntegrante))
