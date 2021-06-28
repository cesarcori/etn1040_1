from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

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
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    grupo = models.CharField(max_length=50, null=True, unique=True)
    nombre_sala_estudiante = models.CharField(max_length=50, null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class DatosTutor(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    nombre_sala_estudiante = models.CharField(max_length=50, null=True)
    fecha_inscripcion= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class DatosEstudiante(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    carnet = models.CharField(max_length=50, null=True, unique=True)
    registro_uni = models.CharField(max_length=50, null=True, unique=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    grupo_doc = models.ForeignKey(DatosDocente,on_delete=models.SET(''), null=True)
    tutor = models.ForeignKey(DatosTutor,on_delete=models.SET(''), null=True)
    # nombre_sala_docente = models.CharField(max_length=50, null=True)
    # nombre_sala_tutor = models.CharField(max_length=50, null=True)
    fecha_inscripcion= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class DatosAdministrador(models.Model):
    usuario = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class Comunicado(models.Model):
    autor = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    tema = models.CharField(max_length=50, null=True)
    texto = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.tema

# class MensajePersonal(models.Model):
    # # REQUIRED_FIELDS = ('autor','destino')
    # autor = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # destino = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    # tema = models.CharField(max_length=50, null=True)
    # texto = models.TextField(blank=True, null=True)
    # fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    # def __str__(self):
        # return self.tema
# Por el momento lo mejor sera crear 4 tablas: est-doc doc-est, est-tut tut-est
# las otras formas de comunicacion seran mediante email. y cosas asi.
# est-doc
# est-tut
# est-adm

# tut-doc
# tut-adm

# doc-adm

# class Conversacion(models.Model):
    # nombre_conversacion = models.CharField(max_length=50, null=True)
    # fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class Para(models.Model):
    nombre_destinatario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre_destinatario.first_name + ' ' + self.nombre_destinatario.last_name
        return self.nombre_completo

class Mensaje(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, null=True)
    para = models.ForeignKey(Para, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'[De: {self.usuario.username};Para:{self.para} mensaje: {self.texto[:20]}'

# practicando el chat segun canales o salas

class Sala(models.Model):
    # el nombre se sala sera dado por id de username en view
    nombre_sala = models.CharField(max_length=50, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.nombre_sala

class MensajeSala(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, null=True)
    sala = models.ForeignKey(Sala, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
