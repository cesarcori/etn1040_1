from django import forms
from .models import *
from proyecto.models import ProyectoDeGrado
#https://drive.google.com/file/d/
from .funciones import *
class SalaRevisarAppForm(forms.ModelForm):
    class Meta:
        model = SalaRevisarApp
        fields = '__all__'
        exclude = ['sala_documento','creado_por','archivo_corregir_web']
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

class NotaSalaRevisarAppForm(forms.ModelForm):
    # maximo = 5
    # nota = forms.DecimalField(min_value=0, max_value=maximo, label = f'',
            # max_digits=2, decimal_places=1)
    class Meta:
        model = NotaSalaRevisarApp
        fields = ['nota_max','nota']
        labels = {
                'nota': 'Nota asignada',
                'nota_max': 'Calificar sobre'
                }

# class NotaSeminarioForm(forms.ModelForm):
    # nota_expos_seminarios = forms.IntegerField(min_value=0, max_value=6,label='Exposiciones o Seminarios (Max. 6%)')
    # class Meta:
        # model = ProyectoDeGrado
        # fields = ['nota_expos_seminarios']
