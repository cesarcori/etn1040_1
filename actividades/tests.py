from django.test import TestCase
from django.utils import timezone
from .models import *

class ActividadTest(TestCase):
    def create_actividad(self, nombre="estudiar reglamento", 
            nombre_humano="Se debe estudiar el reglamento",
            detalle="El estudiante debe estudiar el reglamento y confirmar su estudio",
            valor=4,
            orden=1):
        return Actividad.objects.create(nombre=nombre,nombre_humano=nombre_humano,
                detalle=detalle, valor=valor, orden=orden, fecha_creacion=timezone.now())
            
    def test_create_actividad(self):
        w = self.create_actividad()
        self.assertTrue(isinstance(w, Actividad))
