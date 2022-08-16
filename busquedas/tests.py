from django.test import TestCase

from django.utils import timezone

from .models import *


class ProyectosInscritosTest(TestCase):
            
    def test_proyectos_inscritos(self):
        w = ProyectosInscritos.objects.create(
            tesistas = 1,
            sigla_id = "etn-101",
            autor = "Juan Marcelo Choque Apaza",
            titulo = """
                    SISTEMA DE CONTROL INTELIGENTE PARA ASILO DE
                    ANCIANOS VIEJITO LINDO, BASADO EN ARDUINO
                    APLICACION MOVIL Y VOZ.
            """,
            mencion = "Control",
            tutor = "Ing. Jordan Aruquipa Pérez",
            docente = "Ing. Mario Rios Fernández",
            resumen = """
                El constante crecimiento de la tecnología electrónica, telecomunicaciones y la
                informática, conlleva a desarrollar sistemas informáticos cada vez más complejos para
                satisfacer las necesidades que existe en la sociedad, el poder brindar confort, seguridad,
                control, supervisión, automatización y optimización, procesos que mejoran la calidad de
                vida.
                Los servicios que ofrece la domótica a nuestro diario vivir sin duda busca el confort y la
                seguridad entre sus principales objetivos, brindando formas de comunicación que actúen
                en la interacción a través de dispositivos que realicen una acción en nuestro hogar. Todas
                estas ventajas se pueden resumir en un aumento de la calidad de vida del propietario del
                hogar o de las personas que lo componen.
                Gracias a la evolución de la tecnología que va contribuyendo al desarrollo de numerosas
                áreas tal el caso de la electrónica e informática que van teniendo un gran desarrollo en
                la domótica y debido a la gran cantidad de empresas que brinda este servicio a un costo
                muy alto y aun poco conocido en nuestro medio es necesario buscar alternativas que nos
                ayuden a tener el control.
                El uso de Teléfonos inteligentes, han ido generando un consumo excesivo en la sociedad,
                donde un gran porcentaje de esta, posee uno de estos dispositivos. La preferencia por
                uno u otro dispositivo varía de las funcionalidades que requiere el usuario o simplemente
                de la condición económica que se posea, es por esto que debemos utilizar todos los
                recursos que nos brindan estos aparatos para elevar nuestra calidad de vida a través de
                aplicaciones que podamos utilizar fácilmente y también utilizando plaquetas electrónica
                llamadas Arduino programables.
                Es por ello que la propuesta del proyecto de aplicación es investigar, modelar, diseñar y
                construir un sistema integrado de control y seguridad compuesto de elementos
                computacionales, que permita a personal autorizadas tener acceso a la información y
                2
                control de la gestión remota, lo cual la hace interesante en un entorno donde existen
                pocas aplicaciones que utilizan esta tecno
            """,
            indice = """
                I N D I C E
                Contenido
                CAPITULO I................................................................................................................................................. 1
                1. INTRODUCCIÓN................................................................................................................................ 1
                1.1. ANTECEDENTES .......................................................................................................................... 2
                1.2. PLANTEAMIENTO DEL PROBLEMA ......................................................................................... 4
                1.3. OBJETIVOS......................................................................................................................................... 5
                1.3.1. OBJETIVO GENERAL................................................................................................................ 5
                1.3.2. OBJETIVOS ESPECÍFICOS................................................................................................. 6
                1.4. JUSTIFICACIÓN............................................................................................................................. 6
                1.4.1. JUSTIFICACIÓN TECNOLOGÍCA ........................................................................................... 6
                1.4.2. FACTIBILIDAD ECONÓMICA .............................................................................................. 6
                1.4.3. JUSTIFICACÍON SOCIAL ..................................................................................................... 7
                1.4.4. JUSTIFICACÍON ACADÉMICA ............................................................................................ 7
                1.5. DELIMITACIÓN .............................................................................................................................. 7
                1.6. METODOLOGÍA ............................................................................................................................. 8
                Fuente: [Harry Jaspe, 2012] ..................................................................................................................... 8
                1.7. FACTIBILIDAD DEL PROYECTO.................................................................................................... 8
                1.7.1 Factibilidad Técnica...................................................................................................................... 8
                1.7.2. Factibilidad económica ............................................................................................................. 10
                1.7.3. Calendarización ......................................................................................................................... 13
                1.8. ARQUITECTURA DEL SISTEMA INICIAL ................................................................................... 13
                1.8.1. ENTRADAS ................................................................................................................................ 13
                1.8.2. SALIDAS..................................................................................................................................... 13
                1.8.3. FUNCIONES Y PROCESOS.................................................................................................. 13
                1.8.4. ESPECIFICACIÓN INICIAL DEL SISTEMA ............................................................................ 14
                1.9. DETERMINACION DE REQUERIMIENTOS DE LA INFORMACION ..................................... 14
                1.9.1 REQUERIMIENTOS BASICOS................................................................................................ 14
                1.9.2 SUB PROCESOS BASICOS .................................................................................................... 15
                1.10. DIAGRAMA JERARQUICO DE PROCESOS ............................................................................ 19
                CAPITULO II.............................................................................................................................................. 20
                2. FUNDAMENTACIÓN TEÓRICA .................................................................................................... 20
                2.1. INTRODUCCIÓN .............................................................................................................................. 20
                2.2 DOMOTICA......................................................................................................................................... 20
                2.3 Gestión Energética ............................................................................................................................ 21
                2.3.1 Confort.......................................................................................................................................... 21
                2.3.2 Seguridad..................................................................................................................................... 22
                2.3.3 Comunicación.............................................................................................................................. 22
                2.3.4 Accesibilidad................................................................................................................................ 22
                2.4 ARDUINO............................................................................................................................................ 23
                2.4.1 Características ............................................................................................................................ 25
                2.4.2 Alimentación de un Arduino ...................................................................................................... 26
                2.4.3 Memoria ....................................................................................................................................... 27
                2.4.4 Entradas y Salidas...................................................................................................................... 28
                2.4.5 Comunicaciones ......................................................................................................................... 29
                2.4.6 Programación. ............................................................................................................................. 30
                2.4.7 Reinicio automático por Software ............................................................................................ 31
                2.4.8 Protección contra sobre Corrientes en USB .......................................................................... 32
                2.4.9 Características físicas y compatibilidad de Shields .............................................................. 32
                2.5 SEGURIDAD ...................................................................................................................................... 33
                2.5.1 Gestión de Seguridad en el hogar ........................................................................................... 34
                2.5.2 Vigilancia Interna y Externa ...................................................................................................... 35
                2.5.3 Seguridad Perimetral ................................................................................................................. 36
                2.5.4 Seguridad Periférica................................................................................................................... 36
                2.5.5 Seguridad Volumétrica .............................................................................................................. 37
                2.5.6 Control de Acceso ...................................................................................................................... 37
                2.5.7 Alarma de Agresión.................................................................................................................... 38
                2.5.8 Centrales de Alarma .................................................................................................................. 38
                2.6 SENSORES ........................................................................................................................................ 39
                2.6.1 Sensores de Infrarrojos ................................................................................................................. 40
                2.6.2 Sensores de Ultrasonidos ......................................................................................................... 41
                2.6.3 Sensores de Temperatura......................................................................................................... 42
                2.7 SERVOMOTORES ............................................................................................................................ 43
                2.8 ACCIONAMIENTO DE DISPOSITIVOS ELECTRÓNICOS POR VOZ..................................... 44
                CAPITUL0 III ............................................................................................................................................. 47
                3. DESARROLLO DEL TRABAJO......................................................................................................... 47
                3.1 INTRODUCCIÓN ........................................................................................................................... 47
                3.2 ARQUITECTURA DEL CONTROL DOMOTICO ...................................................................... 47
                3.2.1 Arquitectura centralizada....................................................................................................... 47
                3.2 MODELO DE SISTEMA.................................................................................................................... 48
                3.2.1 Entrada......................................................................................................................................... 48
                3.2.2 Proceso ........................................................................................................................................ 49
                3.2.3 Salida............................................................................................................................................ 49
                3.3 HARDWARE DEL SISTEMA ........................................................................................................... 49
                3.3.1 Materiales .................................................................................................................................... 50
                3.3.2 Modulo Bluetooth HC-05 ........................................................................................................... 51
                3.3.3 Control de Servomotor............................................................................................................... 53
                3.3.4 Sensor de Temperatura............................................................................................................. 53
                3.4. SOFTWARE DEL SISTEMA ........................................................................................................... 55
                3.4.1. Aplicación Móvil ......................................................................................................................... 55
                3.4.2. Interfaz de Inicio ........................................................................................................................ 57
                3.5 INTEFAZ DEL MODULO HC-05 ..................................................................................................... 58
                3.6 Configuración.................................................................................................................................. 58
                3.7 Conexión ......................................................................................................................................... 60
                3.8 CIRCUITO FINAL .............................................................................................................................. 61
                3.9 PROTOTIPO....................................................................................................................................... 62
                3.10 DESARROLLO DEL SISTEMA EN PROTEUS .......................................................................... 63
                3.11 PRUEBAS......................................................................................................................................... 64
                3.11.1 Implementación ........................................................................................................................ 64
                3.11.2 Pruebas de aceptación............................................................................................................ 64
                3.12. Interpretación de pruebas ......................................................................................................... 70
                CAPITULO IV ............................................................................................................................................ 72
                4 CONCLUSIONES Y RECOMENDACIONES.................................................................................... 72
                4.1 CONCLUSIONES......................................................................................................................... 72
                4.2. RECOMENDACIONES.................................................................................................................... 73
                BIBLIOGRAFIA ......................................................................................................................................... 74
                ANEXOS 1................................................................................................................................................. 76
            """,
            bibliografia = """
                74
                BIBLIOGRAFIA
                Valentina Aguirre Muñoz (2013), Prototipo de sistema de control domótico por medio de
                dispositivos Android, utilizando Processing: Trabajo de Grado Universidad
                Católica de Manizales, Facultad de Ingeniería y Arquitectura Ingeniería
                Telemática.
                Emilio Lledó Sánchez (2012), Diseño de un control domótico basado en Arduino:
                Universidad Técnica de Valencia, España
                Arduino (2015), Arduino Página Oficial: http:/www.arduino.ccs
                Android (2014), Android Página Oficial: http:/www.android.com
                Jesús Rodarte Dávila, Jenaro Carlos Paz Gutiérrez, José Saúl González Campos,
                Ramsés Román García Martínez (2013), Casa inteligente y segura (fase 2),
                (Colección Textos Universitarios, Serie Investigación) Universidad Autónoma de
                Ciudad Juárez, Mexico
                Rimaluz (2009), Niveles de iluminación, Recuperado de: http:/www.rimaluz.com/niv-
                _vivienda.html.
                Domótica (2014), Domótica: Servicios para el hogar, Recuperado
                de:
                http:/www.domotive.com/servicios_hogar.htm.
                Adesva Tecnología (2010), Empresa en infraestructuras domótica, Recuperado de
                http://www.adesvatecnologia.com/home.php.
                Mario Rodríguez Cerezo (2014), Sistema de Control remoto para aplicaciones domóticas
                a través de internet: Proyecto final de Carrera Universidad Autónoma de Madrid,
                Escuela Politécnica Superior
                Panta J. (2012), Control Domótico por voz, Escuela Técnica Superior de Ingeniería
                Informática
                Universidad Politécnica de Valencia, Recuperado
                de:
                https://riunet.upv.es/bitstream/handle/10251/17631/ Memoria.pdf?sequence=1
                Coronel, R. (2014), Diseño e implementación de un sistema domótico para un control de
                energía eléctrica. Universidad Mayor de San Andres, Bolivia.
                Lleida (2013), Reconocimiento automatico del habla, Recuperado de
                http://dihana.cps.unizar.es/investigacion/voz/rahframe.html 03/05/2013
                75
                Prieto Francisca, Martinez Eustaquio (2012). Domotización con hardware abierto:
                Arduino & Shields, Facultad Politecnica, Universidad Nacional del Este. Ciudad del Este,
                Paraguay.
                CIEC - Colegio de Ingenieros Especialistas de Córdoba CD (2012), Guía de contenidos
                mínimos para la elaboración de un proyecto de domótica”, Argentina
                doboro J.M. (2010), Manual de Domótica, Recuperado
                de:
                http://www.ramonmillan.com/libros/libroManualDomotica.php
                Sensores (2011), Sensores de movimiento, Recuperado
                de:
                http://sensmovimiento.blogspot.com/p/sensor-de-movimiento.html.
                Ruiz J.M. (2013), Arduino+Ethernet Shield, Recuperado
                de:
                http://unicarlos.com/_ARDUINO/Arduino%20+%20Ethernet%20Shield%20%281
                %29.pdf
                CasaDomo (2014), Domótica, Arquitectura Centralizada, Recuperado
                de:
                http://antoniopendolema.blogspot.com/2013/04/arquitectura-centralizada.html
                Alonso, J.C. (2010) Arduino, Recuperado de: http://arduino.cc.e
                Electrónica (2009), Control de acceso casero con teclado matricial y PIC18F452
                Recuperado de:
                http://blog.bricogeek.com/tag/acceso
                Electrónicos (2013), Motores y servos, Recuperado
                de:
                http://www.electronicoscaldas.com/motores-y-servos/468-micro-servo-motor-
                sg90.htm
                Pérez V. (2010), Contribución al diseño de sistemas domóticos y de entretenimiento
                utilizando hardware libre y software de código abierto, Tesi
            """,
            tipo = "perfil",
            estado = "concluido",
            fecha_inicio = timezone.now(),
            fecha_concluida = timezone.now(),
            fecha_creacion = timezone.now(),  
        )

        self.assertTrue(isinstance(w, ProyectosInscritos))
