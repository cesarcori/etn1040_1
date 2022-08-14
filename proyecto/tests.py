from django.test import TestCase
from django.utils import timezone

from .models import *

class SolicitudInvitadoTest(TestCase):
            
    def test_solicitud_invitado(self):
        usuario = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        w = SolicitudInvitado.objects.create(
            usuario = usuario,
            correo = "test@gmail.com",
            nombre = "Ricardo",
            apellido = "Jordan Rodriguez",
            carnet = "6001234",
            extension = "L.P.",
            registro_uni = "8374653",
            celular = "73675872",
            mencion = "Sistemas de Contol",
            fecha_solicitud = timezone.now(),
        )

        self.assertTrue(isinstance(w, SolicitudInvitado))

class DatosDocenteTest(TestCase):
            
    def test_solicitud_invitado(self):
        usuario = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        w = DatosDocente.objects.create(
            usuario = usuario,
            correo = "test@gmail.com",
            nombre = "Ricardo",
            apellido = "Jordan Rodriguez",
            celular = "73675872",
            mencion = "Sistemas de Contol",
            grupo = "B",
            firma = 'firmas/firma_default.jpg',
            imagen_perfil = "imagenes/profile1.png",
            fecha_inscripcion = timezone.now(),
        )

        self.assertTrue(isinstance(w, DatosDocente))
