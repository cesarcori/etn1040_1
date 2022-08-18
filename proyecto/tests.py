from django.test import TestCase
from django.utils import timezone

from .models import *
from actividades.models import Actividad

class SolicitudInvitadoTest(TestCase):
            
    def test_solicitud_invitado(self):
        usuario = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        w = SolicitudInvitado.objects.create(
            usuario = usuario,
            correo = "test@gmail.com",
            nombre = "Ricardo",
            apellido = "Jordan Rodriguez",
            carnet = "6001234",
            extension = "L.P.",
            registro_uni = "8374653",
            celular = "73675872",
            mencion = "Sistemas de Contol",
            fecha_solicitud = timezone.now(),
        )

        self.assertTrue(isinstance(w, SolicitudInvitado))

class DatosDocenteTest(TestCase):
            
    def test_datos_docente(self):
        usuario = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        w = DatosDocente.objects.create(
            usuario = usuario,
            correo = "test@gmail.com",
            nombre = "Ricardo",
            apellido = "Jordan Rodriguez",
            celular = "73675872",
            mencion = "Sistemas de Contol",
            grupo = "B",
            firma = 'firmas/firma_default.jpg',
            imagen_perfil = "imagenes/profile1.png",
            fecha_inscripcion = timezone.now(),
        )

        self.assertTrue(isinstance(w, DatosDocente))

class DatosDirectorTest(TestCase):
            
    def test_datos_director(self):
        usuario = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        w = DatosDirector.objects.create(
            usuario = usuario,
            correo = "test@gmail.com",
            nombre = "Ricardo",
            apellido = "Jordan Rodriguez",
            celular = "73675872",
            imagen_perfil = "imagenes/profile1.png",
            fecha_inscripcion = timezone.now(),
        )

        self.assertTrue(isinstance(w, DatosDirector))

class DatosTutorTest(TestCase):
            
    def test_datos_tutor(self):
        usuario = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        w = DatosTutor.objects.create(
            usuario = usuario,
            correo = "test@gmail.com",
            nombre = "Ricardo",
            apellido = "Jordan Rodriguez",
            celular = "73675872",
            firma = 'firmas/firma_default.jpg',
            imagen_perfil = "imagenes/profile1.png",
            fecha_inscripcion = timezone.now(),
        )

        self.assertTrue(isinstance(w, DatosTutor))

class DatosTribunalTest(TestCase):
            
    def test_datos_tribunal(self):
        usuario = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        mencion1 = Mencion.objects.create(nombre="Telecomunicación", fecha_creacion = timezone.now())
        mencion2 = Mencion.objects.create(nombre="Sistemas de Control", fecha_creacion = timezone.now())
        w = DatosTribunal.objects.create(
            usuario = usuario,
            correo = "test@gmail.com",
            nombre = "Ricardo",
            apellido = "Jordan Rodriguez",
            celular = "73675872",
            firma = 'firmas/firma_default.jpg',
            imagen_perfil = "imagenes/profile1.png",
            fecha_inscripcion = timezone.now(),
        )
        w.menciones.add(mencion1)
        w.menciones.add(mencion2)

        self.assertTrue(isinstance(w, DatosTribunal))

class DatosEstudianteTest(TestCase):
            
    def test_datos_estudiante(self):
        usuario = User.objects.create(first_name="Ricardo", last_name="Jordan Rodriguez")
        docente = DatosDocente.objects.create(
                usuario = usuario,
                correo = "test@gmail.com",
                nombre = "Ricardo",
                apellido = "Jordan Rodriguez",
                celular = "73675872",
                mencion = "Sistemas de Contol",
                grupo = "B",
                firma = 'firmas/firma_default.jpg',
                imagen_perfil = "imagenes/profile1.png",
                fecha_inscripcion = timezone.now(),
                )
        tutor = DatosTutor.objects.create(
                usuario = usuario,
                correo = "test@gmail.com",
                nombre = "Ricardo",
                apellido = "Jordan Rodriguez",
                celular = "73675872",
                firma = 'firmas/firma_default.jpg',
                imagen_perfil = "imagenes/profile1.png",
                fecha_inscripcion = timezone.now(),
                )
        tribunal = DatosTribunal.objects.create(
                usuario = usuario,
                correo = "test@gmail.com",
                nombre = "Ricardo",
                apellido = "Jordan Rodriguez",
                celular = "73675872",
                firma = 'firmas/firma_default.jpg',
                imagen_perfil = "imagenes/profile1.png",
                fecha_inscripcion = timezone.now(),
                )
        equipo = Equipo.objects.create(
                nombre = "Equipo Transistores",
                alias = "Equipo de transistores",
                cantidad = 3,
                docente = docente, 
                tutor = tutor,
                tutor_acepto = False,
                solicitud_tribunal_docente = False,
                nota_final = 60,
                is_concluido = False,
                nivel_ie = 0.789,
                fecha_conclusion = timezone.now(),
                fecha_creacion = timezone.now(),
                )
        equipo.tribunales.add(tribunal)

        actividad1 = Actividad.objects.create(
                nombre="estudiar reglamento", 
                nombre_humano="Se debe estudiar el reglamento",
                detalle="El estudiante debe estudiar el reglamento y confirmar su estudio",
                valor=4,
                orden=1,
                )

        w = DatosEstudiante.objects.create(
            usuario = usuario,
            correo = "test@gmail.com",
            nombre = "Ricardo",
            apellido = "Jordan Rodriguez",
            carnet = "6001234",
            extension = "L.P.",
            registro_uni = "8374653",
            celular = "73675872",
            mencion = "Sistemas de Contol",
            grupo_doc = docente,
            imagen_perfil = "imagenes/profile1.png",
            imagen_perfil_web = "https://p16-va-default.akamaized.net/img/musically-maliva-obj/1665282759496710~c5_720x720.jpeg",
            modalidad = "INDIVIDUAL",
            is_modalidad_aprobada = False,
            equipo = equipo, 
            is_concluido = False,
            nivel_ie = 0.791,
            fecha_inscripcion = timezone.now(),
        )
        w.actividad.add(actividad1)

        self.assertTrue(isinstance(w, DatosEstudiante))


class EquipoTest(TestCase):
            
    def test_equipo(self):
        w = Equipo.objects.create(
            nombre = "Equipo Marco",
            alias = "Los Transistores",
            cantidad = 2,
            # docente = models.ForeignKey(DatosDocente,on_delete=models.SET_NULL, null=True, blank=True)
            # tutor = models.ForeignKey(DatosTutor,on_delete=models.SET_NULL, null=True, blank=True)
            tutor_acepto = False,
            solicitud_tribunal_docente = False,
            # tribunales = models.ManyToManyField(DatosTribunal, blank=True)
            nota_final = 80,
            is_concluido = False,
            nivel_ie = 0.8879,
            fecha_conclusion = timezone.now(),
            fecha_creacion = timezone.now()
        )

        self.assertTrue(isinstance(w, Equipo))

class MaterialDocenteTest(TestCase):
            
    def test_material_docente(self):
        w = MaterialDocente.objects.create(
            material_docente = 'material_docente/',
        )

        self.assertTrue(isinstance(w, MaterialDocente))

class VistaMaterialDocenteTest(TestCase):
            
    def test_vista_material_docente(self):
        w = VistaMaterialDocente.objects.create(
        )

        self.assertTrue(isinstance(w, VistaMaterialDocente))

class DatosEstudianteTituladoTest(TestCase):
            
    def test_datos_estudiante_titulado(self):
        w = DatosEstudianteTitulado.objects.create(
            correo = "ejemplo@gmail.com",
            nombre = "Alfredo",
            apellido = "Morales Alanoca",
            carnet = "7009836",
            extension = "L.P.",
            registro_uni = "9876153",
            celular = "75693457",
            mencion = "Sistemas de Computación",
            tutor = "Ramiro Mendieta Orellana",
            docente = "Esteban Salazar Molina",
            imagen_perfil = "imagenes/profile1.png",
            fecha_conclusion = timezone.now()
        )

        self.assertTrue(isinstance(w, DatosEstudianteTitulado))

class DatosAdministradorTest(TestCase):
            
    def test_datos_administrador(self):
        w = DatosAdministrador.objects.create(
            correo = "ejemplo@gmail.com",
            nombre = "Alfredo",
            apellido = "Morales Alanoca",
            celular = "75693457",
            imagen_perfil = "imagenes/profile1.png",
            fecha_inscripcion = timezone.now()
        )

        self.assertTrue(isinstance(w, DatosAdministrador))
