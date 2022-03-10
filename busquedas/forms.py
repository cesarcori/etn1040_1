from django import forms

from .models import *

class ProyectosInscritosForm(forms.ModelForm):
    class Meta:
        model = ProyectosInscritos
        fields = '__all__'
        widgets = {
                'autor': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        'placeholder':'Nombre del autor del Perfil o Proyecto de Grado'}),
                'titulo': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        'placeholder':'Título del Perfil o Proyecto de Grado'}),
                'tutor': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        'placeholder':'Nombre del tutor'}),
                'docente': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        'placeholder':'Ingresar nombre del docente ETN-1040'}),
                'resumen': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Resumen del Proyecto de Grado...'}), 
                'indice': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Índice del Proyecto de Grado...'}), 
                'bibliografia': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Bibliografía del Proyecto de Grado...'}), 
                'fecha_inicio': forms.DateInput(
                format=('%d-%m-%Y'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
                'fecha_concluida': forms.DateInput(
                attrs={'class': 'form-control', 
                    'type': 'date'
                    }),
                }
        labels = {
                'autor': 'Autor',
                'titulo': 'Titulo',
                'tutor': 'Tutor',
                'docente': 'Docente',
                'resumen': 'Resumen',
                'indice': 'Índice',
                'bibliografia': 'Bibliografía',
                'perfil_proyecto' : 'Documento'
                }
