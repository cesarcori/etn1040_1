from django import forms
from .models import *

class SubirDocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['archivo']
        # widgets = {
            # 'archivo': forms.FileInput(attrs={'class':'form-control'}),
        # }
        # labels = {
                # 'Documento': 'Subir archivo',
                # }
