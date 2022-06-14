from django import forms
from .models import *
from proyecto.models import ProyectoDeGrado, RegistroPerfil

from .funciones import *

class SalaRevisarDocForm(forms.ModelForm):
    class Meta:
        model = SalaRevisarDoc
        fields = ['asunto','detalle','nota_max']
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
                'nota_max': 'Calificar sobre',
                }

class SalaRevisarDocSinNotaForm(forms.ModelForm):
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
                'nota_max': 'Calificar sobre',
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
        model = SalaRevisarDoc
        fields = ['nota']
        labels = {
                'nota': 'Calificar',
                # 'nota_max': 'Calificar sobre'
                }

class NotaMaxForm(forms.ModelForm):
    class Meta:
        model = SalaRevisarDoc
        fields = ['nota_max']
        labels = {
                'nota_max': 'Calificar sobre'
                }

class SubirDocumentoForm(forms.ModelForm):
    class Meta:
        model = SalaRevisarDoc
        fields = ['archivo_corregir']
        widgets = {
            'archivo_corregir': forms.FileInput(attrs={'class':'form-control',}),
            }
        labels = {
                }

class crearRevisarDocPersonalizadoForm(forms.ModelForm):
    class Meta:
        model = RevisarDocPersonalizado
        fields = ['orden','asunto','detalle','nota_max']
        widgets = {
            'asunto': 
            forms.TextInput(attrs={'class':'input-group input-group-lg',
            'placeholder':'Escribe el asunto...'}),
            'detalle': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control',
            'placeholder':'Escribe las modificaciones...',}),
            }
        labels = {
                'asunto': (''),
                'detalle': (''),
                'nota_max': 'Calificar sobre',
                }

class crearRevisarDocPersonalizadoRevisorForm(forms.ModelForm):
    class Meta:
        model = RevisarDocPersonalizado
        fields = ['orden','asunto','detalle']
        widgets = {
            'asunto': 
            forms.TextInput(attrs={'class':'input-group input-group-lg',
            'placeholder':'Escribe el asunto...'}),
            'detalle': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control',
            'placeholder':'Escribe las modificaciones...',}),
            }
        labels = {
                'asunto': (''),
                'detalle': (''),
                }

class RegistroPerfilForm(forms.ModelForm):
    class Meta:
        model = RegistroPerfil
        fields = '__all__'
        exclude = ['equipo']
        widgets = {
                'titulo': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        'placeholder':'Título del perfil...'}),
                'resumen': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Resumen del perfil...'}), 
                'indice': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Índice del perfil...'}), 
                'bibliografia': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Bibliografía del perfil...'}), 
                'perfil': forms.FileInput(attrs={'class':'form-control'}),
                }
        labels = {
                'titulo': '',
                'resumen': '',
                'indice': '',
                'bibliografia': '',
                'perfil': 'Subir archivo del perfil',
                }

class RegistroProyectoDeGradoForm(forms.ModelForm):
    class Meta:
        model = ProyectoDeGrado
        fields = '__all__'
        exclude = ['equipo','calificacion','nota_tiempo_elaboracion',
                'nota_expos_seminarios','nota_informes_trabajo',
                'nota_cumplimiento_cronograma']
        widgets = {
                'titulo': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        'placeholder':'Título del Proyecto de Grado...'}),
                'resumen': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Resumen del Proyecto de Grado...'}), 
                'indice': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Índice del Proyecto de Grado...'}), 
                'bibliografia': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Bibliografía del Proyecto de Grado...'}), 
                'archivo': forms.FileInput(attrs={'class':'form-control',}),
                }
        labels = {
                'titulo': '',
                'resumen': '',
                'indice': '',
                'bibliografia': '',
                'archivo': 'Subir archivo del Proyecto de Grado',
                }

