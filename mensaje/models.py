from django.db import models
from django.contrib.auth.models import User, Group

class CanalPar(models.Model):
    TIPO = {
            ('MENSAJE','MENSAJE'),
            ('OBSERVAR','OBSERVAR'),
            }
    de = models.ForeignKey(User, related_name='de', null=True, blank=True, on_delete=models.CASCADE)
    para = models.ForeignKey(User, related_name='para', null=True, blank=True, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=200, choices=TIPO, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.nombre_sala

class MensajePar(models.Model):
    texto = models.TextField(blank=True, null=True)
    visto = models.BooleanField(default=False)
    canal = models.ForeignKey(CanalPar, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
