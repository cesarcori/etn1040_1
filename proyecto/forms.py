from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.core.validators import RegexValidator
from django.db.utils import OperationalError

class CreateUserForm(UserCreationForm):
    solo_carnet = RegexValidator(r'^[0-9]{7,8}$', 'Ingresar solo numero')
    solo_letra= RegexValidator(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1 a-zA-ZÀ-ÿ\u00f1\u00d1]*$', 'Ingresar solo letras')
    solo_ru = RegexValidator(r'^[0-9]{7}$', 'Ingresar un R.U. de 7 dígitos')
    solo_celular = RegexValidator(r'^[6|7][0-9]{7}$', 
            'Ingresar un numero de celular')

    try:
        MENCION = [(m,m) for m in Mencion.objects.all()]
    except OperationalError:
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
    solo_grupo= RegexValidator(r'^[A-Z]$', 'Ingresar una sola letra mayúscula,\
            hasta grupo Z')
    solo_letra= RegexValidator(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1 a-zA-ZÀ-ÿ\u00f1\u00d1]*$', 'Ingresar solo letras')
    nombre = forms.CharField(max_length = 50, validators=[solo_letra])
    apellido = forms.CharField(max_length = 50, validators=[solo_letra])
    correo = forms.EmailField(max_length=100)
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

class RegistroPerfilForm(forms.ModelForm):
    class Meta:
        model = RegistroPerfil
        fields = '__all__'
        exclude = ['equipo',]
        widgets = {
                'titulo': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        'placeholder':'Título del perfil...'}),
                'resumen': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Resumen del perfil...'}), 
                'perfil': forms.FileInput(attrs={'class':'form-control'}),
                }
        labels = {
                'titulo': '',
                'resumen': '',
                'perfil': 'Subir archivo del perfil',
                }

class ActividadesCronogramaForm(forms.ModelForm):
    solo_numero = RegexValidator(r'^([1-9]|10){1,3}$', 'solo se admite 3 digitos')
    class Meta:
        model = ActividadesCronograma
        fields = '__all__'
        exclude = ['equipo',]
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
        exclude = ['equipo',]

class ProyectoDeGradoForm(forms.ModelForm):
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
                'archivo': forms.FileInput(attrs={'class':'form-control',}),
                }
        labels = {
                'titulo': '',
                'resumen': '',
                'archivo': 'Subir archivo del Proyecto de Grado',
                }

class RegistroProyectoTribunalForm(forms.ModelForm):
    class Meta:
        model = RegistroProyectoTribunal
        fields = '__all__'
        exclude = ['equipo','nota', 'nota_final']
        widgets = {
                'titulo': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        'placeholder':'Título del Proyecto de Grado...'}),
                'resumen': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    'placeholder':'Resumen del Proyecto de Grado...'}), 
                'archivo': forms.FileInput(attrs={'class':'form-control',}),
                }
        labels = {
                'titulo': '',
                'resumen': '',
                'archivo': '',
                }

class CalificarProyectoForm(forms.Form):
    nota1= forms.IntegerField(min_value=0, max_value=9,label='Tiempo de Elaboración (Max. 9%)')
    nota2= forms.IntegerField(min_value=0, max_value=6,label='Exposiciones o Seminarios (Max. 6%)')
    nota3= forms.IntegerField(min_value=0, max_value=22,label='Informes de Trabajo (Max. 22%)')
    nota4= forms.IntegerField(min_value=0, max_value=3,label='Cumplimiento de Cronograma (Max. 3%)')

class CalificarProyectoTribunalForm(forms.ModelForm):
    nota = forms.IntegerField(min_value=0, max_value=60,label='Nota (Max. 60%)')
    class Meta:
        model = NotaTribunal
        fields = ['nota']

class DatosTutorForm(forms.ModelForm):
    class Meta:
        model = DatosTutor
        fields = '__all__'
        exclude = ['usuario','correo','firma']
class DatosDocenteForm(forms.ModelForm):
    class Meta:
        model = DatosDocente
        fields = ['celular', 'imagen_perfil']
class DatosEstudianteForm(forms.ModelForm):
    class Meta:
        model = DatosEstudiante
        fields = ['celular','imagen_perfil','imagen_perfil_web']
class DatosAdministradorForm(forms.ModelForm):
    class Meta:
        model = DatosAdministrador
        fields = ['celular','imagen_perfil']
class DatosDirectorForm(forms.ModelForm):
    class Meta:
        model = DatosDirector
        fields = '__all__'
        exclude =['usuario']
class DatosTribunalForm(forms.ModelForm):
    class Meta:
        model = DatosTribunal
        fields = '__all__'
        exclude = ['usuario','correo','firma']
# class BusquedaProyectoForm(forms.ModelForm):
    # class Meta:
        # model = BusquedaProyecto
        # fields = '__all__'
        # # exclude = ['usuario','calificacion']
        # widgets = {
                # 'autor': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        # 'placeholder':'Nombre del autor del Perfil o Proyecto de Grado'}),
                # 'titulo': forms.TextInput(attrs={'class':'input-group input-group-lg',
                        # 'placeholder':'Titulo del Perfil o Proyecto de Grado'}),
                # 'resumen': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    # 'placeholder':'Resumen del Proyecto de Grado...'}), 
                # 'indice': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    # 'placeholder':'Índice del Proyecto de Grado...'}), 
                # 'bibliografia': forms.Textarea(attrs={'rows':3, 'class':'form-control', 
                    # 'placeholder':'Bibliografía del Proyecto de Grado...'}), 
                # }
        # labels = {
                # 'autor': 'Autor',
                # 'titulo': 'Titulo',
                # 'resumen': 'Resumen',
                # 'indice': 'Índice',
                # 'bibliografia': 'Bibliografía',
                # 'perfil_proyecto' : 'Documento'
                # }
class TutorForm(forms.ModelForm):
    class Meta:
        model = DatosTutor
        fields = ['correo']
class TribunalForm(forms.ModelForm):
    class Meta:
        model = DatosTribunal
        fields = ['correo']
        # fields = '__all__'
        # exclude = ['usuario','imagen_perfil','celular',]
# class AuspicioForm(forms.ModelForm):
    # class Meta:
        # model = Auspicio
        # fields = '__all__'
        # exclude = ['usuario']
# class FirmasForm(forms.ModelForm):
    # class Meta:
        # model = Firmas
        # fields = '__all__'
        # exclude = ['usuario']

class FirmaTutorForm(forms.ModelForm):
    class Meta:
        model = DatosTutor
        fields = ['firma']
class FirmaDocenteForm(forms.ModelForm):
    class Meta:
        model = DatosTutor
        fields = ['firma']

class DocumentosForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = '__all__'
        exclude = ['usuario','firma_formulario1_doc','firma_formulario2_doc','firma_formulario4_doc']
class DocumentosDocenteForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = ['firma_formulario1_doc','firma_formulario2_doc','firma_formulario4_doc']
