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

    EXTENSION = [
        ( 'LP'  ,  'La Paz' )     ,
        ( 'SC'  ,  'Santa Cruz' ) ,
        ( 'OR'  ,  'Oruro' )      ,
        ( 'CB'  ,  'Cochabamba' ) ,
        ( 'CH'  ,  'Chuquisaca' ) ,
        ( 'PT'  ,  'Potosí' )     ,
        ( 'TJ'  ,  'Tarija' )     ,
        ( 'BE'  ,  'Beni' )       ,
        ( 'PD'  ,  'Pando' )      ,
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
    extension = forms.ChoiceField(choices=EXTENSION)
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
        widgets = {
    'tema':forms.TextInput(attrs={'class':'input-group input-group-lg',
    'placeholder':'Escribe el asunto...'}),
    'texto': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control',
    'placeholder':'Escribe el comunicado para los estudiantes...',}),
                  }
        labels = {
        'tema': ('Asunto'),
        'texto': ('Comunicado'),
                }

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
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows':2,
        'class':'form-control', 'placeholder':'Escribe el mensaje...'}),
        label='')

class MaterialDocenteForm(forms.ModelForm):
    class Meta:
        model = MaterialDocente
        fields = '__all__'
        exclude = ['propietario',]

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
    # 'material_estudiante': forms.FileInput(attrs={'class':'form-control'}),
                }
        labels = {
                'sala': ('Asunto de la revisión:'),
                'texto': ('Detalles revisión:'),
'material_estudiante': ('Subir perfil en pdf con los cambios resaltado en\
amarillo'),
                }

class SalaRevisarProyectoForm(forms.ModelForm):
    class Meta:
        model = SalaRevisarProyecto
        fields = '__all__'
        exclude = ['docente_rev','tutor_rev','estudiante_rev','sala_revisar']
        widgets = {
    'sala': 
    forms.TextInput(attrs={'class':'input-group input-group-lg',
    'placeholder':'Asunto del Proyecto de Grado...'}),
    'texto': forms.Textarea(attrs={ 'rows': 3, 'class': 'form-control',
    'placeholder':'Escribe tus modificaciones que elaboraste en el Proyecto de Grado...',}),
    'material_estudiante': forms.FileInput(attrs={'class':'form-control',}),
    'material_estudiante': forms.FileInput(attrs={'class':'form-control'}),
                }
        labels = {
                'sala': ('Asunto de la revisión:'),
                'texto': ('Detalles revisión:'),
'material_estudiante': ('Subir Proyecto de Grado en pdf con los cambios resaltado en amarillo'),
                }

class MensajeDocenteRevisarForm(forms.ModelForm):
    class Meta:
        model = MensajeDocenteRevisar
        fields = ['texto']
        widgets = {
                'texto': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Correcciones que debe realizar...'}), 
                }
        labels = {
                'texto': ''
                }

class MensajeDocenteRevisarProyectoForm(forms.ModelForm):
    class Meta:
        model = MensajeDocenteRevisarProyecto
        fields = ['texto']
        widgets = {
                'texto': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Correcciones que debe realizar al Proyecto de Grado...'}), 
                }
        labels = {
                'texto': ''
                }

class MensajeTutorRevisarForm(forms.ModelForm):
    class Meta:
        model = MensajeTutorRevisar
        fields = ['texto']
        widgets = {
                'texto': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Correcciones que debe realizar...'}), 
                }
        labels = {
                'texto': ''
                }
        
class MensajeTutorRevisarProyectoForm(forms.ModelForm):
    class Meta:
        model = MensajeTutorRevisarProyecto
        fields = ['texto']
        widgets = {
                'texto': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Correcciones que debe realizar...'}), 
                }
        labels = {
                'texto': ''
                }

class RegistroPerfilForm(forms.ModelForm):
    class Meta:
        model = RegistroPerfil
        fields = '__all__'
        exclude = ['usuario',]
        widgets = {
                'titulo': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        'placeholder':'Copia el título del perfil...'}),
                'resumen': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Copia el resumen del perfil...'}), 
                }
        labels = {
                'titulo': 'Titulo del Perfil',
                'resumen': 'Resumen del Perfil',
                }

class ActividadesCronogramaForm(forms.ModelForm):
    solo_numero = RegexValidator(r'^([1-9]|10){1,3}$', 'solo se admite 3 digitos')
    class Meta:
        model = ActividadesCronograma
        fields = '__all__'
        exclude = ['usuario',]
        widgets = {
                'actividad': forms.TextInput(attrs={
                        'placeholder':'Actividad a elaborar'}),
                }
        labels = {
                'actividad': '',
                }

class RegistroCronogramaForm(forms.ModelForm):
    class Meta:
        model = RegistroCronograma
        fields = '__all__'
        exclude = ['usuario',]

class ProyectoDeGradoForm(forms.ModelForm):
    class Meta:
        model = ProyectoDeGrado
        fields = '__all__'
        exclude = ['usuario','calificacion']
        widgets = {
                'titulo': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        'placeholder':'Copia el título del Proyecto de Grado...'}),
                'resumen': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Copia el resumen del Proyecto de Grado...'}), 
                }
        labels = {
                'titulo': 'Titulo del Proyecto de Grado',
                'resumen': 'Resumen del Proyecto de Grado',
                }

class CalificarProyectoForm(forms.Form):
    calificacion = forms.IntegerField(min_value=1, max_value=40)

class DatosTutorForm(forms.ModelForm):
    class Meta:
        model = DatosTutor
        fields = '__all__'
        exclude = ['usuario','correo']
class DatosDocenteForm(forms.ModelForm):
    class Meta:
        model = DatosDocente
        fields = ['celular', 'imagen_perfil']
class DatosEstudianteForm(forms.ModelForm):
    class Meta:
        model = DatosEstudiante
        fields = ['celular','imagen_perfil']
class DatosAdministradorForm(forms.ModelForm):
    class Meta:
        model = DatosAdministrador
        fields = ['celular','imagen_perfil']
