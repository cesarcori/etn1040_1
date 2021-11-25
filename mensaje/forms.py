from django import forms
from .models import *

class MensajeParForm(forms.ModelForm):
    class Meta:
        model = MensajePar
        fields = ['texto']
        texto = forms.CharField(widget=forms.Textarea(attrs={'rows':2,
        'class':'form-control', 'placeholder':'Escribe el mensaje...'}),
        label='')
        widgets = {
        'texto': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control',
        'placeholder':'Escribir mensaje...',}),
                    }
        labels = {
                    'texto': (''),
                    }
