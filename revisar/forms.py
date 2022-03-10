from django import forms
from .models import *
#https://drive.google.com/file/d/
class SalaRevisarAppForm(forms.ModelForm):
    class Meta:
        model = SalaRevisarApp
        fields = '__all__'
        exclude = ['sala_documento','creado_por','archivo_corregir']
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
'archivo_corregir': ('Subir el docmento en pdf con los cambios resaltado en\
amarillo'),
                }

class MensajeRevisarAppForm(forms.ModelForm):
    class Meta:
        model = MensajeRevisarApp
        fields = ['mensaje']
        widgets = {
                'mensaje': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Escribe un mensaje...'}), 
                }
        labels = {
                'mensaje': ''
                }
