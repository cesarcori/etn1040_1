from django.db import models
from django.contrib.auth.models import User


class Actividad(models.Model):
    nombre = models.CharField(max_length=50, null=True)
    nombre_humano = models.CharField(max_length=100, null=True)
    detalle = models.TextField(blank=True, null=True)
    valor = models.PositiveSmallIntegerField(null=True, blank=True, default=1)
    orden = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        ordering = ['orden']
    def __str__(self):
        return f'Orden: {self.orden} - Actividad: {self.nombre} - Valor: {self.valor}'

class AvisoActividad(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    equipo = models.ForeignKey("proyecto.Equipo", null=True, blank=True, on_delete=models.CASCADE)
    visto = models.BooleanField(default=False)
    actividades = models.ManyToManyField(Actividad, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'Aviso para: {self.usuario} - De: {self.equipo}'

class ActividadHistorial(models.Model):
    equipo = models.ForeignKey("proyecto.Equipo", null=True, blank=True, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'Orden: {self.actividad.orden} - Actividad: {self.actividad.nombre} - Equipo: {self.equipo}'

