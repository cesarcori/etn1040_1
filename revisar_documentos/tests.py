from django.test import TestCase

from django.utils import timezone

from .models import *


class SalaDocumentoDocTest(TestCase):
    def test_sala_documento_doc(self):
        w = SalaDocumentoDoc.objects.create(
            visto_bueno = False,
            tipo = "perfil",
            updated = timezone.now(),
            fecha_creacion = timezone.now(),
        )

        self.assertTrue(isinstance(w, SalaDocumentoDoc))

class ConfiguracionSalaTest(TestCase):
    def test_configuracion_sala(self):
        w = ConfiguracionSala.objects.create(
            is_predeterminado = False,
        )

        self.assertTrue(isinstance(w, ConfiguracionSala))

class SalaRevisarDocTest(TestCase):
    def test_sala_revisar_doc(self):
        equipo = Equipo.objects.create(
                nombre = "Equipo Transistores",
                alias = "Equipo de transistores",
                cantidad = 3,
                # docente = docente, 
                # tutor = tutor,
                tutor_acepto = False,
                solicitud_tribunal_docente = False,
                nota_final = 60,
                is_concluido = False,
                nivel_ie = 0.789,
                fecha_conclusion = timezone.now(),
                fecha_creacion = timezone.now(),
                )
        grupo_revisor = Group.objects.create(name="tutor")
        sala_documento = SalaDocumentoDoc.objects.create(
            equipo = equipo,
            grupo_revisor = grupo_revisor,
            visto_bueno = False,
            tipo = "perfil",
            updated = timezone.now(),
            fecha_creacion = timezone.now(),
        )
        w = SalaRevisarDoc.objects.create(
            sala_documento = sala_documento,
            asunto = "Primera revision",
            detalle = "Mandar toda la informacion que recabaste",
            archivo_corregir = 'material_estudiante_perfil/perfil_borrador.pdf',
            nota = 14,
            nota_max = 16,
            is_calificado = True,
            fecha_creacion = timezone.now(),
        )

        self.assertTrue(isinstance(w, SalaRevisarDoc))

class MensajeRevisarDocTest(TestCase):
    def test_mensaje_revisar_doc(self):
        w = MensajeRevisarDoc.objects.create(
            mensaje = "Falta mejorar las observaciones.",
            visto = False,
            fecha_creacion = timezone.now()
        )

        self.assertTrue(isinstance(w, MensajeRevisarDoc))

class NotaSalaRevisarDocTest(TestCase):
    def test_nota_sala_revisar_doc(self):
        w = NotaSalaRevisarDoc.objects.create(
            nota = 15,
            nota_max = 20,
        )

        self.assertTrue(isinstance(w, NotaSalaRevisarDoc))

class RevisarDocPredeterminadoTest(TestCase):
    def test_revisar_doc_predeterminado(self):
        w = RevisarDocPredeterminado.objects.create(
            orden = 1,
            asunto = "Capitulo 1: INTRODUCCIÓN",
            detalle = "Completar la introduccion del documento",
            tipo = "proyecto",
            nota_max = 14,
            fecha_creacion = timezone.now()
        )

        self.assertTrue(isinstance(w, RevisarDocPredeterminado))

class RevisarDocPersonalizadoTest(TestCase):
    def test_revisar_doc_personalizado(self):
        w = RevisarDocPersonalizado.objects.create(
            orden = 1,
            asunto = "Capitulo 1: INTRODUCCIÓN",
            detalle = "Completar la introduccion del documento",
            tipo = "proyecto",
            nota_max = 14,
            fecha_creacion = timezone.now()
        )

        self.assertTrue(isinstance(w, RevisarDocPersonalizado))
