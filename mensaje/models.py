from django.db import models
from django.contrib.auth.models import User, Group

class CanalPar(models.Model):
    de = models.ForeignKey(User, related_name='de', null=True, blank=True, on_delete=models.CASCADE)
    para = models.ForeignKey(User, related_name='para', null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"De: {self.de}, Para: {self.para}"

class MensajePar(models.Model):
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, null=True)
    is_visto = models.BooleanField(default=False)
    canal = models.ForeignKey(CanalPar, null=True, blank=True, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return f"Mensaje: {self.texto} - {self.canal}"

# class Canal(models.Model):
    # usuarios = models.ManyToManyField(User, related_name='canales', blank=True)
    # fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    # # def __str__(self):
        # # return f"Canal: {self.usuarios}"

# class Mensaje(models.Model):
    # usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # texto = models.TextField(blank=True, null=True)
    # is_visto = models.BooleanField(default=False)
    # canal = models.ForeignKey(Canal, null=True, blank=True, on_delete=models.CASCADE)
    # fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    # def __str__(self):
        # return f"Mensaje: {self.texto} - {self.canal}"
