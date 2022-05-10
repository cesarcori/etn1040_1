from django.db import models
from proyecto.models import Equipo

class TituloPerfil(models.Model):
    equipo = models.OneToOneField(Equipo, null=True, blank=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=True)
