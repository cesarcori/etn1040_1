from django.db import models
from proyecto.models import *

class Solicitud(models.Model):
    estudiante = models.ForeignKey(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    docente = models.ForeignKey(DatosDocente, null=True, blank=True, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=50, null=True, blank=True, default='Solicitud de Modalidad Múltiple')
    detalle = models.TextField(null=True)
    visto = models.BooleanField(default=False)
    aprobar = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'Estudiante: {self.estudiante} - Docente: {self.docente}'

class RechazarSolicitud(models.Model):
    estudiante = models.ForeignKey(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    docente = models.ForeignKey(DatosDocente, null=True, blank=True, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=50, null=True, blank=True, default='Solicitud Rechazada')
    detalle = models.TextField(null=True)
    visto = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'Estudiante: {self.estudiante} - Docente: {self.docente}'

class SolicitudIntegrante(models.Model):
    estudiante_interesado = models.ForeignKey(DatosEstudiante, related_name="interesado", null=True, blank=True, on_delete=models.CASCADE)
    estudiante_invitado = models.ForeignKey(DatosEstudiante, related_name="invitado", null=True, blank=True, on_delete=models.CASCADE)
    correo_invitado = models.EmailField(max_length=100, null=True)
    visto = models.BooleanField(default=False)
    aprobar = models.BooleanField(default=False)
    rechazar = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'Estudiante interesado: {self.estudiante_interesado} - Equipo: {self.estudiante_invitado}'

