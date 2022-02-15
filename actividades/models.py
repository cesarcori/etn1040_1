from django.db import models
# from proyecto.models import *

class Actividad(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    valor = models.PositiveSmallIntegerField(null=True, blank=True, default=1)
    # orden = models.PositiveSmallIntegerField(null=True, blank=True, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    # class Meta:
        # ordering = ['-orden']
    def __str__(self):
        return f'Actividad: {self.nombre} - Valor: {self.valor}'

# class RealizarActividad(models.Model):
    # actividad = models.ForeignKey(Actividad, null=True, blank=True, on_delete=models.CASCADE)
    # estudiante = models.ForeignKey(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    # hecho = models.BooleanField(default=False)
    # def __str__(self):
        # return f'Actividad: {self.actividad.nombre} - Hecho: {self.hecho} - Estudiante: {self.estudiante}'
