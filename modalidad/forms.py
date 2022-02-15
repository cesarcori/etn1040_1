from django import forms
from .models import *
from proyecto.models import Equipo


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['asunto','detalle']
        widgets = {
    'asunto':forms.TextInput(attrs={'class':'input-group input-group-lg',
    'placeholder':'Escribe el asunto...'}),
    'detalle': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control',
    'placeholder':'Escribe a detalle sobre qué trata tu tema y cual es el argumento que el Tutor menciona para que el proyecto sea elaborado por más integrantes. Junto al número de participantes que recomienda',}),
                  }
        labels = {
        'asunto': (''),
        'detalle': (''),
                }

class AprobarSolicitudForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['cantidad']

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre']

class RechazarSolicitudForm(forms.ModelForm):
    class Meta:
        model = RechazarSolicitud
        fields = ['asunto','detalle']
        widgets = {
    'asunto':forms.TextInput(attrs={'class':'input-group input-group-lg',
    'placeholder':'Escribe el asunto...'}),
    'detalle': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control',
    'placeholder':'Escribe a detalle por qué no se puede realizar la modalidad múltiple',}),
                  }
        labels = {
        'asunto': (''),
        'detalle': (''),
                }

