from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.core.validators import RegexValidator

class CreateUserForm(UserCreationForm):
    solo_carnet = RegexValidator(r'^[0-9]{7,8}$', 'Ingresar solo numero')
    solo_letra= RegexValidator(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1 a-zA-ZÀ-ÿ\u00f1\u00d1]*$', 'Ingresar solo letras')
    solo_ru = RegexValidator(r'^[0-9]{7}$', 'Ingresar un R.U. de 7 dígitos')
    solo_celular = RegexValidator(r'^[6|7][0-9]{7}$', 
            'Ingresar un numero de celular')

    s = 'Sistemas de Computación'
    t = 'Telecomunicación'
    c = 'Control'
    MENCION = [
        (s, s),
        (t, t),
        (c, c),
    ] 
    class Meta:
        model = User
        fields = [
                'username',
                'email', 
                'password1', 
                'password2',
                ]
    nombre = forms.CharField(max_length = 200, validators=[solo_letra])
    apellido = forms.CharField(max_length = 200, validators=[solo_letra])
    carnet = forms.CharField(max_length = 200, validators=[solo_carnet])
    registro_uni = forms.CharField(max_length = 200, 
                    label='Registro Universitario', validators=[solo_ru])
    celular = forms.CharField(max_length = 200, validators=[solo_celular])
    mencion = forms.ChoiceField(choices=MENCION)

class Habilitar(forms.Form):
    habilitar = forms.BooleanField(label='')

class FormDocente(forms.Form):
    s = 'Sistemas de Computación'
    t = 'Telecomunicación'
    c = 'Control'
    MENCION = [
        (s, s),
        (t, t),
        (c, c),
    ] 
    solo_grupo= RegexValidator(r'^[A-F]$', 'Ingresar una sola letra mayúscula,\
            hasta grupo F')
    solo_letra= RegexValidator(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1 a-zA-ZÀ-ÿ\u00f1\u00d1]*$', 'Ingresar solo letras')
    nombre = forms.CharField(max_length = 50, validators=[solo_letra])
    apellido = forms.CharField(max_length = 50, validators=[solo_letra])
    grupo = forms.CharField(max_length = 50, validators=[solo_grupo])
    mencion = forms.ChoiceField(choices=MENCION)

class ComunicadoForm(forms.ModelForm):
    class Meta:
        model = Comunicado
        fields = ('tema', 'texto',)

class MensajeEstudianteForm(forms.Form):
    d = 'Docente'
    t = 'Tutor'
    PARA = [
           (d, d),
           (t, t),
            ]
    texto = forms.CharField(widget=forms.Textarea)
    para = forms.ChoiceField(choices=PARA)

class MensajeForm(forms.Form):
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':25}))

# class MaterialDocenteForm(forms.Form):
    # propietario = form.
    # material_docente = forms.FileField()
class MaterialDocenteForm(forms.ModelForm):
    class Meta:
        model = MaterialDocente
        fields = '__all__'
        exclude = ['propietario',]

class MaterialEstudianteForm(forms.ModelForm):
    class Meta:
        model = MaterialEstudiante
        fields = '__all__'
        exclude = ['sala']
        widgets = {
        # 'texto': forms.Textarea(attrs={'rows': 2, 'cols': 25}),
        'texto': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control',
'placeholder':'Escribe tus modificaciones que elaboraste en el perfil...',}),
        'material_estudiante': forms.FileInput(attrs={'class':'form-control',}),
                  }
        labels = {
                'texto': ('Enviar Perfil'),
'material_estudiante': ('Subir perfil en pdf con los cambios resaltado en\
amarillo'),
                }
class SalaRevisarForm(forms.ModelForm):
    class Meta:
        model = SalaRevisar
        fields = '__all__'
        exclude = ['docente_rev','tutor_rev','estudiante_rev','sala_revisar']
        widgets = {
    'sala': 
    forms.TextInput(attrs={'class':'input-group input-group-lg',
    'placeholder':'Escribe el nombre de la sala...'}),
    'texto': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control',
    'placeholder':'Escribe tus modificaciones que elaboraste en el perfil...',}),
    'material_estudiante': forms.FileInput(attrs={'class':'form-control',}),
    'material_estudiante': forms.FileInput(attrs={'class':'form-control'}),
                }
        labels = {
                'sala': ('Asunto de la revisión:'),
                'texto': ('Detalles revisión:'),
'material_estudiante': ('Subir perfil en pdf con los cambios resaltado en\
amarillo'),
                }
