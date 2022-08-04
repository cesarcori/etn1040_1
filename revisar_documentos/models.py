from django.db import models
from django.contrib.auth.models import User, Group
from proyecto.models import DatosEstudiante, Equipo

TIPO_DOCUMENTO = [
    ('perfil','Perfil'),
    ('proyecto','Borrador de Proyecto'),
    ('tribunal','Proyecto Final Tribunal'),
]
class SalaDocumentoDoc(models.Model):
    revisor = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    grupo_revisor = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, null=True, blank=True, on_delete=models.CASCADE)
    visto_bueno = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50, choices=TIPO_DOCUMENTO, null=True)
    # updated = models.DateTimeField(auto_now=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.titulo = self.revisor.first_name
        return f'Tipo: {self.tipo}, Revisor: {self.grupo_revisor.__str__()}, Equipo: {self.equipo.__str__()}'

class ConfiguracionSala(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    is_predeterminado = models.BooleanField(default=True)

class SalaRevisarDoc(models.Model):
    sala_documento = models.ForeignKey(SalaDocumentoDoc, null=True, blank=True, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=200, null=True)
    detalle = models.TextField(blank=True, null=True)
    archivo_corregir = models.FileField(upload_to='material_estudiante_perfil/', null=True, blank=True)
    nota = models.DecimalField(null=True, blank=True, default=0, max_digits=3, decimal_places=1)
    nota_max = models.DecimalField(null=True, blank=True, default=0, max_digits=3, decimal_places=1)
    is_calificado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Sala Asunto: {self.asunto}'

class MensajeRevisarDoc(models.Model):
    sala = models.ForeignKey(SalaRevisarDoc, null=True, blank=True, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    mensaje = models.TextField(blank=True, null=True)
    visto = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Sala Revisar: {self.sala}, De: {self.usuario}, Mensaje: {self.mensaje},'

class NotaSalaRevisarDoc(models.Model):
    sala = models.ForeignKey(SalaRevisarDoc, null=True, blank=True, on_delete=models.CASCADE)
    revisor = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    nota = models.DecimalField(null=True, blank=True, default=0, max_digits=3, decimal_places=1)
    nota_max = models.DecimalField(null=True, blank=True, default=0, max_digits=3, decimal_places=1)

class RevisarDocPredeterminado(models.Model):
    orden = models.PositiveSmallIntegerField(null=True)
    asunto = models.CharField(max_length=200, null=True)
    detalle = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=50, choices=TIPO_DOCUMENTO, null=True)
    nota_max = models.DecimalField(null=True, blank=True, default=0, max_digits=3, decimal_places=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-orden']

    def __str__(self):
        return f'Asunto: {self.asunto}'

class RevisarDocPersonalizado(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    orden = models.PositiveSmallIntegerField(null=True)
    asunto = models.CharField(max_length=200, null=True)
    detalle = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=50, choices=TIPO_DOCUMENTO, null=True)
    nota_max = models.DecimalField(null=True, blank=True, default=0, max_digits=3, decimal_places=1)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-orden']

    def __str__(self):
        return f'Asunto: {self.asunto}'
