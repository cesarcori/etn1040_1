from django import forms
from proyecto.models import Auspicio

class AuspicioForm(forms.ModelForm):
    class Meta:
        model = Auspicio
        fields = '__all__'
        exclude = ['usuario']
