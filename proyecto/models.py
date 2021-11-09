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
    extension = models.CharField(max_length=50, null=True)
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
    firma = models.ImageField(default='firmas/firma_default.jpg', upload_to='firmas/', null=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class DatosDirector(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True, blank=True)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    apellido = models.CharField(max_length=50, null=True, blank=True)
    celular = models.CharField(max_length=50, null=True, blank=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)
    # def __str__(self):
        # self.nombre_completo = self.nombre + ' ' + self.apellido
        # return self.nombre_completo

class MaterialDocente(models.Model):
    propietario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    material_docente = models.FileField(upload_to='material_docente/', null=True)

class VistaMaterialDocente(models.Model):
    usuario = models.ForeignKey('DatosEstudiante', null=True, blank=True, on_delete=models.CASCADE)
    docente = models.ForeignKey(DatosDocente, null=True, blank=True, on_delete=models.CASCADE)
    material_docente_visto = models.ForeignKey(MaterialDocente, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        self.identificador = self.usuario.__str__() +' - '+ self.material_docente_visto.__str__()
        return self.identificador

class MensajeDocenteRevisar(models.Model):
    texto = models.TextField(blank=True, null=True)
    visto_docente = models.BooleanField(default=False)
    visto_estudiante = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    sala = models.ForeignKey('SalaRevisar', null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class MensajeDocenteRevisarProyecto(models.Model):
    texto = models.TextField(blank=True, null=True)
    visto_docente = models.BooleanField(default=False)
    visto_estudiante = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    sala = models.ForeignKey('SalaRevisarProyecto', null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class MensajeTutorRevisar(models.Model):
    texto = models.TextField(blank=True, null=True)
    visto_tutor = models.BooleanField(default=False)
    visto_estudiante = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    sala = models.ForeignKey('SalaRevisar', null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class MensajeTutorRevisarProyecto(models.Model):
    texto = models.TextField(blank=True, null=True)
    visto_tutor = models.BooleanField(default=False)
    visto_estudiante = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    sala = models.ForeignKey('SalaRevisarProyecto', null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class SalaRevisar(models.Model):
    sala = models.CharField(max_length=50, null=True)
    docente_rev= models.ForeignKey(DatosDocente, null=True, blank=True, on_delete=models.CASCADE)
    tutor_rev= models.ForeignKey('DatosTutor', null=True, blank=True, on_delete=models.CASCADE)
    estudiante_rev= models.ForeignKey('DatosEstudiante', null=True, blank=True, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, null=True)
    material_estudiante = models.FileField(upload_to='material_estudiante_perfil/', null=True)
    material_corregido_docente = models.FileField(upload_to='material_estudiante_perfil/', null=True, blank=True)
    material_corregido_tutor  = models.FileField(upload_to='material_estudiante_perfil/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.sala

class SalaRevisarProyecto(models.Model):
    sala = models.CharField(max_length=50, null=True)
    docente_rev= models.ForeignKey(DatosDocente, null=True, blank=True, on_delete=models.CASCADE)
    tutor_rev= models.ForeignKey('DatosTutor', null=True, blank=True, on_delete=models.CASCADE)
    estudiante_rev= models.ForeignKey('DatosEstudiante', null=True, blank=True, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, null=True)
    material_estudiante = models.FileField(upload_to='material_estudiante_proyecto/', null=True)
    material_corregido_docente = models.FileField(upload_to='material_estudiante_perfil/', null=True, blank=True)
    material_corregido_tutor  = models.FileField(upload_to='material_estudiante_perfil/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.sala

class SalaRevisarTribunal(models.Model):
    sala = models.CharField(max_length=50, null=True)
    tribunal_rev= models.ForeignKey('DatosTribunal', null=True, blank=True, on_delete=models.CASCADE)
    estudiante_rev= models.ForeignKey('DatosEstudiante', null=True, blank=True, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, null=True)
    material_estudiante = models.FileField(upload_to='material_estudiante_proyecto/', null=True)
    visto_bueno = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.sala

class DatosTutor(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    firma = models.ImageField(default='firmas/firma_default.jpg', upload_to='firmas/', null=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    fecha_inscripcion= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class DatosTribunal(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    firma = models.ImageField(default='firmas/firma_default.jpg', upload_to='firmas/', null=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
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
    extension = models.CharField(max_length=50, null=True)
    registro_uni = models.CharField(max_length=50, null=True, unique=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    grupo_doc = models.ForeignKey(DatosDocente,on_delete=models.SET(''), null=True)
    tutor = models.ForeignKey(DatosTutor,on_delete=models.SET(''), null=True, blank=True)
    tutor_acepto = models.BooleanField(default=False)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    vb_perfil_docente = models.BooleanField(default=False)
    vb_perfil_tutor = models.BooleanField(default=False)
    vb_proyecto_docente = models.BooleanField(default=False)
    vb_proyecto_tutor = models.BooleanField(default=False)
    solicitud_tribunal_docente = models.BooleanField(default=False)
    tribunales = models.ManyToManyField(DatosTribunal)
    fecha_inscripcion= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class Tribunal_1_Estudiante(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    tribunal_1 = models.ForeignKey(DatosTribunal, null=True, blank=True, on_delete=models.CASCADE)

class Tribunal_2_Estudiante(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    tribunal_2 = models.ForeignKey(DatosTribunal, null=True, blank=True, on_delete=models.CASCADE)

class DatosEstudianteTitulado(models.Model):
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    carnet = models.CharField(max_length=50, null=True, unique=True)
    extension = models.CharField(max_length=50, null=True)
    registro_uni = models.CharField(max_length=50, null=True, unique=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    tutor = models.CharField(max_length=100, null=True)
    docente = models.CharField(max_length=100, null=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    fecha_conclusion= models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        return self.nombre_completo

class DatosAdministrador(models.Model):
    usuario = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
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

class VistaReglamento(models.Model):
    usuario = models.ForeignKey(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    reglamento_visto = models.ForeignKey(Reglamento, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        self.identificador = self.usuario.__str__() +' - '+ self.reglamento_visto.__str__()#+' - Visto: '+ self.visto.__str__()
        return self.identificador

class RegistroPerfil(models.Model):
    usuario = models.OneToOneField(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=True)
    resumen = models.TextField(blank=True, null=True)
    perfil = models.FileField(upload_to='perfiles/', null=True)
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

class ProyectoDeGrado(models.Model):
    usuario = models.OneToOneField(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=True)
    resumen = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='proyectos/', null=True)
    nota_tiempo_elaboracion = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_expos_seminarios = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_informes_trabajo = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_cumplimiento_cronograma = models.PositiveSmallIntegerField(null=True, blank=True)
    calificacion = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class Auspicio(models.Model):
    usuario = models.OneToOneField(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=200, default='', null=True,blank=True)
    supervisor = models.CharField(max_length=200, default='', null=True,blank=True)
    cargo = models.CharField(max_length=200, default='', null=True,blank=True)

class Progreso(models.Model):
    usuario = models.OneToOneField(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    nivel = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class BusquedaProyecto(models.Model):
    documento = {
            ('perfil','Perfil'),
            ('proyecto','Proyecto'),
            }
    autor = models.CharField(max_length=200, null=True)
    titulo = models.CharField(max_length=200, null=True)
    resumen = models.TextField(blank=True, null=True)
    indice = models.TextField(blank=True, null=True)
    bibliografia = models.TextField(blank=True, null=True)
    perfil_proyecto = models.CharField(max_length=200, choices=documento, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class Mencion(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.nombre

# class Firmas(models.Model):
    # usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # firma = models.ImageField(default='firmas/firma_default.jpg', upload_to='firmas/', null=True)

class Documentos(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firma_carta_aceptacion = models.BooleanField(default=False)
    firma_formulario1= models.BooleanField(default=False)
    firma_carta_conclusion= models.BooleanField(default=False)
    firma_formulario2 = models.BooleanField(default=False)
    firma_formulario3 = models.BooleanField(default=False)
    firma_formulario4 = models.BooleanField(default=False)
    # firma docente
    firma_formulario1_doc= models.BooleanField(default=False)
    firma_formulario2_doc = models.BooleanField(default=False)
    firma_formulario4_doc = models.BooleanField(default=False)

