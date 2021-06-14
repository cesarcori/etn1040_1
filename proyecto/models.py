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
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class DatosDocente(models.Model):
    usuario = models.CharField(max_length=50, null=True, unique=True)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    grupo = models.CharField(max_length=50, null=True, unique=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class DatosEstudiante(models.Model):
    usuario = models.CharField(max_length=50, null=True, unique=True)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    carnet = models.CharField(max_length=50, null=True, unique=True)
    registro_uni = models.CharField(max_length=50, null=True, unique=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    grupo_doc = models.ForeignKey(DatosDocente,on_delete=models.SET('sin docente'), null=True)
    fecha_inscripcion= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class DatosTutor(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    fecha_inscripcion= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class DatosAdministrador(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

