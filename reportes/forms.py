from django import forms
from .models import *

class TituloPerfilForm(forms.ModelForm):
    class Meta:
        model = TituloPerfil
        fields = ['titulo']
        widgets = {
    'titulo':forms.TextInput(attrs={'class':'input-group input-group-lg',
    'placeholder':'Escribe el título del perfil de proyecto de grado'}),
                  }
        labels = {
        'titulo': 'Título de Perfil de Proyecto de Grado',
                }
