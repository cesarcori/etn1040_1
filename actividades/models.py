from django.db import models
# from proyecto.models import *

class Actividad(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    detalle = models.TextField(blank=True, null=True)
    valor = models.PositiveSmallIntegerField(null=True, blank=True, default=1)
    orden = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        ordering = ['orden']
    def __str__(self):
        return f'Orden: {self.orden} - Actividad: {self.nombre} - Valor: {self.valor}'

