from django.test import TestCase
from django.utils import timezone
from .models import *

class ActividadTest(TestCase):
    def create_actividad(self, 
            nombre="estudiar reglamento", 
            nombre_humano="Se debe estudiar el reglamento",
            detalle="El estudiante debe estudiar el reglamento y confirmar su estudio",
            valor=4,
            orden=1
            ):
        return Actividad.objects.create(nombre=nombre,nombre_humano=nombre_humano,
                detalle=detalle, valor=valor, orden=orden, fecha_creacion=timezone.now())
            
    def test_create_actividad(self):
        w = self.create_actividad()
        self.assertTrue(isinstance(w, Actividad))

class ActividadHistorialTest(TestCase):
    def test_create_actividad(self):
        # no se necesito de Equipo. 
        actividad = Actividad.objects.create(
                nombre="estudiar reglamento", 
                nombre_humano="Se debe estudiar el reglamento",
                detalle="El estudiante debe estudiar el reglamento y confirmar su estudio",
                valor=4,
                orden=1,
                )
        w = ActividadHistorial.objects.create(
                # equipo = equipo,
                actividad = actividad,
                fecha_creacion = timezone.now(),
                )
        self.assertTrue(isinstance(w, ActividadHistorial))

class AvisoActividadTest(TestCase):
    def test_aviso_actividad(self):
        usuario = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        actividad = Actividad.objects.create(
                nombre="estudiar reglamento", 
                nombre_humano="Se debe estudiar el reglamento",
                detalle="El estudiante debe estudiar el reglamento y confirmar su estudio",
                valor=4,
                orden=1,
                )
        w = AvisoActividad.objects.create(
                usuario = usuario,
                # equipo =
                visto = False,
                # actividades = many ot many
                fecha_creacion = timezone.now(),
                )
        w.actividades.add(actividad)
        self.assertTrue(isinstance(w, AvisoActividad))
