from django.db import models

class ProyectosInscritos(models.Model):
    TIPO = [
            ('perfil','Perfil'),
            ('proyecto','Proyecto'),
            ]
    ESTADO = [
            ('concluido','Concluido'),
            ('en proceso','En proceso'),
            ]
    autor = models.CharField(max_length=200, null=True)
    titulo = models.CharField(max_length=200, null=True)
    tutor = models.CharField(max_length=200, null=True)
    docente = models.CharField(max_length=200, null=True)
    resumen = models.TextField(blank=True, null=True)
    indice = models.TextField(blank=True, null=True)
    bibliografia = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=200, choices=TIPO, default='proyecto', null=True)
    estado = models.CharField(max_length=200, choices=ESTADO, default='concluido', null=True)
    fecha_inicio = models.DateTimeField(null=True,blank=True)
    fecha_concluida = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

class ProyectosExcel(models.Model):
    TIPO = [
            ('perfil','Perfil'),
            ('proyecto','Proyecto'),
            ]
    ESTADO = [
            ('concluido','Concluido'),
            ('en proceso','En proceso'),
            ]
    MENCION = [
            ('telecomunicacion','Telecomunicación'),
            ('control','Control'),
            ('sistemas','Sistemas de Computación'),
            ]
    tesistas = models.SmallIntegerField(null=True)
    sigla_id = models.CharField(max_length=200, null=True, unique=True)
    autor = models.CharField(max_length=200, null=True)
    titulo = models.CharField(max_length=200, null=True)
    mencion = models.CharField(max_length=200, choices=MENCION, default='proyecto', null=True)
    tutor = models.CharField(max_length=200, null=True)
    docente = models.CharField(max_length=200, null=True)
    resumen = models.TextField(blank=True, null=True)
    indice = models.TextField(blank=True, null=True)
    bibliografia = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=200, choices=TIPO, default='proyecto', null=True)
    estado = models.CharField(max_length=200, choices=ESTADO, default='concluido', null=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_concluida = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
