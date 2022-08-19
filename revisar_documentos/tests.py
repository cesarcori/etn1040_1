from django.test import TestCase

from django.utils import timezone

from .models import *


class SalaDocumentoDocTest(TestCase):
    def test_sala_documento_doc(self):
        w = SalaDocumentoDoc.objects.create(
            visto_bueno = False,
            tipo = "perfil",
            updated = timezone.now(),
            fecha_creacion = timezone.now(),
        )

        self.assertTrue(isinstance(w, SalaDocumentoDoc))

class ConfiguracionSalaTest(TestCase):
    def test_configuracion_sala(self):
        w = ConfiguracionSala.objects.create(
            is_predeterminado = False,
        )

        self.assertTrue(isinstance(w, ConfiguracionSala))
