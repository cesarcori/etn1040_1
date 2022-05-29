from django import forms
from .models import *
from proyecto.models import ProyectoDeGrado

from .funciones import *

class SalaRevisarDocForm(forms.ModelForm):
    class Meta:
        model = SalaRevisarDoc
        fields = ['asunto','detalle']
        widgets = {
            'asunto': 
            forms.TextInput(attrs={'class':'input-group input-group-lg',
            'placeholder':'Escribe el asunto...'}),
            'detalle': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control',
            'placeholder':'Escribe las modificaciones...',}),
            'archivo_corregir': forms.FileInput(attrs={'class':'form-control',}),
            }
        labels = {
                'asunto': (''),
                'detalle': (''),
'archivo_corregir': 
    ('Subir el docmento en pdf con los cambios resaltado en amarillo'),
                }

class MensajeRevisarDocForm(forms.ModelForm):
    class Meta:
        model = MensajeRevisarDoc
        fields = ['mensaje']
        widgets = {
                'mensaje': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Escribe un mensaje...'}), 
                }
        labels = {
                'mensaje': ''
                }

class NotaSalaRevisarDocForm(forms.ModelForm):
    class Meta:
        model = NotaSalaRevisarDoc
        fields = ['nota_max','nota']
        labels = {
                'nota': 'Nota asignada',
                'nota_max': 'Calificar sobre'
                }

class NotaMaxForm(forms.ModelForm):
    class Meta:
        model = NotaSalaRevisarDoc
        fields = ['nota_max']
        labels = {
                'nota_max': 'Calificar sobre'
                }

