from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from actividades.models import Actividad

def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Solo Pdf')

class SolicitudInvitado(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.EmailField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    carnet = models.CharField(max_length=50, null=True, unique=True)
    extension = models.CharField(max_length=50, null=True)
    registro_uni = models.CharField(max_length=50, null=True, unique=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class DatosDocente(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.EmailField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    grupo = models.CharField(max_length=50, null=True, unique=True)
    firma = models.ImageField(default='firmas/firma_default.jpg', upload_to='firmas/', null=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class DatosDirector(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.EmailField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    apellido = models.CharField(max_length=50, null=True, blank=True)
    celular = models.CharField(max_length=50, null=True, blank=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class DatosTutor(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.EmailField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    firma = models.ImageField(default='firmas/firma_default.jpg', upload_to='firmas/', null=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    fecha_inscripcion= models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class DatosTribunal(models.Model):
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.EmailField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    menciones = models.ManyToManyField("Mencion", blank=True)
    firma = models.ImageField(default='firmas/firma_default.jpg', upload_to='firmas/', null=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    fecha_inscripcion= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class DatosEstudiante(models.Model):
    MODALIDAD = [
            ('individual','Individual'),
            ('multiple','Múltiple'),
            ]
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.EmailField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    carnet = models.CharField(max_length=50, null=True, unique=True)
    extension = models.CharField(max_length=50, null=True)
    registro_uni = models.CharField(max_length=50, null=True, unique=True)
    celular = models.CharField(max_length=50, null=True)
    mencion = models.CharField(max_length=50, null=True)
    grupo_doc = models.ForeignKey(DatosDocente,on_delete=models.SET_NULL, null=True)
    # tutor = models.ForeignKey(DatosTutor,on_delete=models.SET_NULL, null=True, blank=True)
    # tutor_acepto = models.BooleanField(default=False)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    imagen_perfil_web = models.URLField(max_length=200, null=True, default="https://p16-va-default.akamaized.net/img/musically-maliva-obj/1665282759496710~c5_720x720.jpeg")
    # solicitud_tribunal_docente = models.BooleanField(default=False)
    # tribunales = models.ManyToManyField(DatosTribunal, blank=True)
    modalidad = models.CharField(max_length=200, choices=MODALIDAD, null=True, blank=True)
    is_modalidad_aprobada = models.BooleanField(default=False)
    equipo = models.ForeignKey('Equipo', null=True, blank=True, on_delete=models.SET_NULL)
    actividad = models.ManyToManyField(Actividad, blank=True)
    is_concluido = models.BooleanField(default=False)
    nivel_ie = models.DecimalField(null=True, blank=True, default=0, max_digits=10, decimal_places=5)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    class Meta:
        ordering = ['nivel_ie']

class Equipo(models.Model):
    nombre = models.CharField(max_length=150, null=True, unique=True)
    alias = models.CharField(max_length=50, null=True, unique=True)
    cantidad = models.PositiveSmallIntegerField(null=True, default=2)
    docente = models.ForeignKey(DatosDocente,on_delete=models.SET_NULL, null=True, blank=True)
    tutor = models.ForeignKey(DatosTutor,on_delete=models.SET_NULL, null=True, blank=True)
    tutor_acepto = models.BooleanField(default=False)
    solicitud_tribunal_docente = models.BooleanField(default=False)
    tribunales = models.ManyToManyField(DatosTribunal, blank=True)
    nota_final = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    is_concluido = models.BooleanField(default=False)
    nivel_ie = models.DecimalField(null=True, blank=True, default=0, max_digits=10, decimal_places=5)
    fecha_conclusion = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f'Equipo: {self.nombre}'
    class Meta:
        ordering = ['nivel_ie']

class MaterialDocente(models.Model):
    propietario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    material_docente = models.FileField(upload_to='material_docente/', null=True)
    def __str__(self):
        return f"{self.material_docente}"

class VistaMaterialDocente(models.Model):
    usuario = models.ForeignKey(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    docente = models.ForeignKey(DatosDocente, null=True, blank=True, on_delete=models.CASCADE)
    material_docente_visto = models.ForeignKey(MaterialDocente, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        self.identificador = self.usuario.__str__() +' - '+ self.material_docente_visto.__str__()
        return self.identificador

class DatosEstudianteTitulado(models.Model):
    correo = models.EmailField(max_length=50, null=True, unique=True)
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
        return f"{self.nombre} {self.apellido}"

class DatosAdministrador(models.Model):
    usuario = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    correo = models.EmailField(max_length=50, null=True, unique=True)
    nombre = models.CharField(max_length=50, null=True)
    apellido = models.CharField(max_length=50, null=True)
    celular = models.CharField(max_length=50, null=True)
    imagen_perfil = models.ImageField(default="imagenes/profile1.png", upload_to='imagenes/', null=True)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, null=True)

    # def __str__(self):
        # self.nombre_completo = self.nombre + ' ' + self.apellido
        # return self.nombre_completo

class Comunicado(models.Model):
    autor = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    tema = models.CharField(max_length=50, null=True)
    texto = models.TextField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.tema

# class Sala(models.Model):
    # # el nombre se sala sera dado por id de username en view
    # nombre_sala = models.CharField(max_length=50, null=True)
    # fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    # def __str__(self):
        # return self.nombre_sala

# class MensajeSala(models.Model):
    # usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # texto = models.TextField(blank=True, null=True)
    # is_visto = models.BooleanField(default=False)
    # sala = models.ForeignKey(Sala, null=True, blank=True, on_delete=models.CASCADE)
    # fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

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
    # usuario = models.OneToOneField(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    equipo = models.OneToOneField(Equipo, null=True, blank=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=True)
    resumen = models.TextField(null=True)
    indice = models.TextField(null=True)
    bibliografia = models.TextField(null=True)
    perfil = models.FileField(upload_to='perfiles/', null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

# class Formularios(models.Model):
    # archivo = models.FileField(upload_to='formularios/', null=True,
            # blank=True, validators=[validate_file_extension])

class ActividadesCronograma(models.Model):
    equipo = models.ForeignKey(Equipo, null=True, blank=True, on_delete=models.CASCADE)
    actividad = models.CharField(max_length=200, null=True)
    semana_inicial = models.PositiveSmallIntegerField(null=True)
    semana_final= models.PositiveSmallIntegerField(null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class RegistroCronograma(models.Model):
    equipo = models.OneToOneField(Equipo, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class ProyectoDeGrado(models.Model):
    equipo = models.OneToOneField(Equipo, null=True, blank=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=True)
    resumen = models.TextField(null=True)
    indice = models.TextField(null=True)
    bibliografia = models.TextField(null=True)
    archivo = models.FileField(upload_to='proyectos/', null=True)
    nota_tiempo_elaboracion = models.DecimalField(null=True, blank=True, default=0, max_digits=3, decimal_places=1)
    nota_expos_seminarios = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    nota_informes_trabajo = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_cumplimiento_cronograma = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    calificacion = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class RegistroProyectoTribunal(models.Model):
    equipo = models.OneToOneField(Equipo, null=True, blank=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=True)
    resumen = models.TextField(null=True)
    indice = models.TextField(null=True)
    bibliografia = models.TextField(null=True)
    archivo = models.FileField(upload_to='proyectos/', null=True)
    nota = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class NotaTribunal(models.Model):
    equipo = models.ForeignKey(Equipo, null=True, blank=True, on_delete=models.CASCADE)
    tribunal = models.ForeignKey(DatosTribunal, null=True, blank=True, on_delete=models.CASCADE)
    nota = models.PositiveSmallIntegerField(null=True, blank=True)

class Auspicio(models.Model):
    usuario = models.OneToOneField(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=200, default='', null=True,blank=True)
    supervisor = models.CharField(max_length=200, default='', null=True,blank=True)
    cargo = models.CharField(max_length=200, default='', null=True,blank=True)

class Progreso(models.Model):
    # usuario = models.OneToOneField(DatosEstudiante, null=True, blank=True, on_delete=models.CASCADE)
    equipo = models.OneToOneField(Equipo, null=True, blank=True, on_delete=models.CASCADE)
    nivel = models.PositiveSmallIntegerField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

# class BusquedaProyecto(models.Model):
    # documento = [
            # ('perfil','Perfil'),
            # ('proyecto','Proyecto'),
            # ]
    # autor = models.CharField(max_length=200, null=True)
    # titulo = models.CharField(max_length=200, null=True)
    # resumen = models.TextField(blank=True, null=True)
    # indice = models.TextField(blank=True, null=True)
    # bibliografia = models.TextField(blank=True, null=True)
    # perfil_proyecto = models.CharField(max_length=200, choices=documento, null=True)
    # fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class Mencion(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.nombre

class Documentos(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firma_carta_aceptacion = models.BooleanField(default=False)
    firma_carta_conclusion= models.BooleanField(default=False)
    firma_formulario1= models.BooleanField(default=False)
    firma_formulario2 = models.BooleanField(default=False)
    firma_formulario3 = models.BooleanField(default=False)
    firma_formulario4 = models.BooleanField(default=False)
    # firma docente
    firma_formulario1_doc= models.BooleanField(default=False)
    firma_formulario2_doc = models.BooleanField(default=False)
    firma_formulario4_doc = models.BooleanField(default=False)

