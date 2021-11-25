from django.db import models
from django.contrib.auth.models import User, Group
from proyecto.models import DatosEstudiante

TIPO_REVISAR= [
    ('perfil','Perfil'),
    ('proyecto','Proyecto'),
    ('tribunal','Tribunal'),
    ]
class SalaDocumentoApp(models.Model):
    revisor = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    grupo_revisor = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    visto_bueno = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50, choices=TIPO_REVISAR, null=True)
    def __str__(self):
        self.titulo = self.revisor.first_name
        return f'Documento: {self.tipo}, Revisor: {self.titulo}-{self.grupo_revisor}, Est: {self.estudiante.nombre}'

class SalaRevisarApp(models.Model):
    sala_documento = models.ForeignKey(SalaDocumentoApp, null=True, blank=True, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=200, null=True)
    detalle = models.TextField(blank=True, null=True)
    archivo_corregir = models.FileField(upload_to='material_estudiante_perfil/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'Sala Asunto: {self.asunto}'

class MensajeRevisarApp(models.Model):
    sala = models.ForeignKey(SalaRevisarApp, null=True, blank=True, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    mensaje = models.TextField(blank=True, null=True)
    visto = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'Sala Revisar: {self.sala}, De: {self.usuario}, Mensaje: {self.mensaje},'

# class SalaRevisarApp(models.Model):
    # revisor = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # grupo_revisor = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    # estudiante = models.ForeignKey(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    # tipo = models.CharField(max_length=50, choices=TIPO_REVISAR, null=True)
    # asunto = models.CharField(max_length=200, null=True)
    # detalle = models.TextField(blank=True, null=True)
    # archivo_corregir = models.FileField(upload_to='material_estudiante_perfil/', null=True, blank=True)
    # fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    # def __str__(self):
        # self.titulo = self.revisor.first_name
        # return f'Revisando: {self.tipo}, Revisor: {self.titulo}-{self.grupo_revisor}, Est: {self.estudiante.nombre}'

# class MensajeRevisarApp(models.Model):
    # sala = models.ForeignKey(SalaRevisarApp, null=True, blank=True, on_delete=models.CASCADE)
    # usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # mensaje = models.TextField(blank=True, null=True)
    # visto = models.BooleanField(default=False)
    # fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

