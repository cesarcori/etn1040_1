from django.db import models
from django.contrib.auth.models import User, Group

from proyecto.models import Equipo

class Documento(models.Model):
    TIPO = [
        ('carta_aceptacion','Carta de Aceptación'),
        ('carta_conclusion','Carta de Conclusión'),
        ('formulario_aprobacion','Formulario Aprobación de Perfil'),
        ('formulario_solicitud_tribunal','Formulario de Solicitud de Nombramiento de Tribunal'),
        ('formulario_registro_seguimiento','Formulario de Registro y Seguimiento'),
        ('formulario_materia','Formulario Materia: Proyecto'),
        ('plantilla_observacion','Plantilla de Observación'),
    ]
    equipo = models.ForeignKey(Equipo, null=True, blank=True, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='documentos/', null=True)
    tipo = models.CharField(max_length=200, choices=TIPO, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"Tipo: {self.tipo} - Pertenece a: {self.equipo}"
