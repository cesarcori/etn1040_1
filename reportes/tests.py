from django.test import TestCase

from .models import *

class TituloPerfilTest(TestCase):
            
    def test_titulo_perfil(self):
        w = TituloPerfil.objects.create(
            titulo = models.CharField(max_length=200, null=True, blank=True)
        )

        self.assertTrue(isinstance(w, TituloPerfil))
