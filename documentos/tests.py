from django.test import TestCase
from django.utils import timezone

from .models import *


class DocumentoTest(TestCase):
            
    def test_documento(self):
        w = Documento.objects.create(
            archivo = 'documentos/',
            tipo = 'carta_aceptacion',
            fecha_creacion = timezone.now()
        )

        self.assertTrue(isinstance(w, Documento))
