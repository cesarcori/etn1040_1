from django.db import models
from django.contrib.auth.models import User
class SolicitudInvitado(models.Model):
    usuario = models.CharField(max_length=50, null=True, unique=True)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    carnet = models.CharField(max_length=50, null=True, unique=True)
    registro_uni = models.CharField(max_length=50, null=True, unique=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.usuario

class DatosEstudiante(models.Model):
    usuario = models.CharField(max_length=50, null=True, unique=True)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    carnet = models.CharField(max_length=50, null=True, unique=True)
    registro_uni = models.CharField(max_length=50, null=True, unique=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.usuario

class DatosDocente(models.Model):
    usuario = models.CharField(max_length=50, null=True, unique=True)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    grupo = models.CharField(max_length=50, null=True, unique=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.usuario

class DatosTutor(models.Model):
    usuario = models.CharField(max_length=50, null=True, unique=True)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.usuario



