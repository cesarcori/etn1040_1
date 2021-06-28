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
    solo_grupo= RegexValidator(r'^[A-J]$', 'Ingresar una sola letra mayúscula,\
            hasta la J')
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
    # texto = forms.CharField(widget=forms.Textarea)
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':25}))

