from django.test import TestCase

from django.utils import timezone

from .models import *


class CanalParTest(TestCase):
            
    def test_canal_par(self):
        # usuario1 = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        # usuario2 = User.objects.create(first_name="Jorge", last_name="Aruquipa Rodriguez")
        w = CanalPar.objects.create(
            # de = usuario1,
            # para = usuario2,
            fecha_creacion = timezone.now()
        )

        self.assertTrue(isinstance(w, CanalPar))

class MensajeParTest(TestCase):
            
    def test_mensaje_par(self):
        usuario = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        canal = CanalPar.objects.create(
            fecha_creacion = timezone.now()
        )
        w = MensajePar.objects.create(
            usuario = usuario,
            texto = "Hola estimado, te escribo para ver como anda el proyecto de grado",
            is_visto = False,
            canal = canal,
            fecha_creacion = timezone.now()
        )

        self.assertTrue(isinstance(w, MensajePar))
