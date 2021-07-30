from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Solo Pdf')

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
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class MaterialDocente(models.Model):
    propietario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    material_docente = models.FileField(upload_to='material_docente/', null=True)

class MaterialEstudiante(models.Model):
    sala = models.ForeignKey('SalaRevisar', null=True, blank=True, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, null=True)
    material_estudiante = models.FileField(upload_to='material_estudiante/', null=True)

class MensajeDocenteRevisar(models.Model):
    texto = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    sala = models.ForeignKey('SalaRevisar', null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class MensajeTutorRevisar(models.Model):
    texto = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    sala = models.ForeignKey('SalaRevisar', null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class SalaRevisar(models.Model):
    sala = models.CharField(max_length=50, null=True)
    docente_rev= models.ForeignKey(DatosDocente, null=True, blank=True, on_delete=models.CASCADE)
    tutor_rev= models.ForeignKey('DatosTutor', null=True, blank=True, on_delete=models.CASCADE)
    estudiante_rev= models.ForeignKey('DatosEstudiante', null=True, blank=True, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, null=True)
    material_estudiante = models.FileField(upload_to='material_estudiante/', null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.sala

class CorregirPerfil(models.Model):
    docente_tutor = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    corregir_perfil = models.ForeignKey(MaterialEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    material_para_corregir = models.FileField(upload_to='material_para_corregir/', null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

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

class DatosEstudiante(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    carnet = models.CharField(max_length=50, null=True, unique=True)
    registro_uni = models.CharField(max_length=50, null=True, unique=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    cronograma = models.CharField(max_length=50, null=True)
    grupo_doc = models.ForeignKey(DatosDocente,on_delete=models.SET(''), null=True)
    tutor = models.ForeignKey(DatosTutor,on_delete=models.SET(''), null=True)
    # nombre_sala_docente = models.CharField(max_length=50 null=True)
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

class Reglamento(models.Model):
    archivo = models.FileField(upload_to='reglamentos/', null=True,
            blank=True, validators=[validate_file_extension])
    def __str__(self):
        return self.archivo.name

class RegistroPerfil(models.Model):
    usuario = models.OneToOneField(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=True)
    resumen = models.TextField(blank=True, null=True)
    # cronograma = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class Formularios(models.Model):
    archivo = models.FileField(upload_to='formularios/', null=True,
            blank=True, validators=[validate_file_extension])

class ActividadesCronograma(models.Model):
    usuario = models.ForeignKey(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    actividad = models.CharField(max_length=200, null=True)
    semana_inicial = models.PositiveSmallIntegerField(null=True, blank=True)
    semana_final= models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class RegistroCronograma(models.Model):
    usuario = models.OneToOneField(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

