# Sistema etn1040

Sistema que realiza la administración y búsqueda de proyectos de grado de 
la asignatura **Proyecto de Grado ETN-1040**.

# Sitio de alojamiento implementado

El sistema se encuentra implementado el alojamiento web gratuito:
pythoanywhere, bajo la URL: https://etn1040.pythonanywhere.com/ 

Nota: Todas las pruebas y creaciones de usuario son restablecidad al punto de
del ejemplo cada día a hrs. 12:00 del medio día.

Nombres de usuario y contraseñas de ingreso: 

Administrador: 
    
    usuario: kardex
    contraseña: kardex

Director:

    usuario: bush_director
    contraseña: bush_director 

## Ejemplo del proceso del estudiante.

Ejemplo de actividad estudiantes: Todos los estudiantes tienen la contraseña: masseguro2000

**Paso 1:** Estudio de reglamentos y material del docente.
[Video demo](https://youtu.be/6tp7_CmEVBA) 

    usuario: bethy
    
    usuario: arnol

**Paso 2:** Búsqueda de proyectos de grado.[Video demo](https://youtu.be/KTPyEa9N39A)

Nota: La búsqueda profunda se encuentra rota. El almacenamiento en el 
servidor gratuito es de 500MB y las librerías Python requieren de 600MB aproximadamente. 

    usuario: wilson

    usuario: camila

**Paso 3:** Elección de modalidad y registro de tutoría. [Video demo](https://youtu.be/EDzH-kTm71A)

    usuario: mara

    usuario: milenka

**Paso 4:** Revisión y aprobación del perfil de proyecto de grado [Video demo](https://youtu.be/U7NG-pw7sZw)

    usuario: alejandra

    usuario: ernesto

**Paso 5:** Revisión y evaluación del borrador de proyecto de grado [Video demo](https://youtu.be/y3VgGyQCEeE)

    usuario: pablo

    usuario: israel

**Paso 6:** Revisión y evaluación del proyecto final [Video demo](https://youtu.be/f7nqji2vUwA)

    usuario: ricardo

    usuario: florencia

Docentes: 
```
usuario: pedro123_docente 
contraseña: pedro123_docente 

usuario: alberto123_docente 
contraseña: alberto123_docente

usuario: esteban123_docente 
contraseña: esteban123_docente 

usuario: orlando123_docente
contraseña: orlando123_docente

usuario: ricardo123_docente 
contraseña: ricardo123_docente
```

Tutores: 

```
usuario: arturo2000_tutor
contraseña: arturo2000_tutor

usuario: umsa_romeo_tutor
contraseña: umsa_romeo_tutor

usuario: ingeniero_lozano_tutor
contraseña: ingeniero_lozano_tutor

usuario: miranda123_tutor
contraseña: miranda123_tutor

usuario: ing_nina_tutor
contraseña: ing_nina_tutor

usuario: freddy12345_tutor 
contraseña: freddy12345_tutor

```
Tribunales: 
```
usuario: arturo2000_tribunal
contraseña: arturo2000_tribunal

usuario: enriquecontreras_tribunal
contraseña: enriquecontreras_tribunal

usuario: pedrolazo_tribunal
contraseña: pedrolazo_tribunal

usuario: freddy12345_tribunal
contraseña: freddy12345_tribunal

usuario: ricardo_tribunal
contraseña: ricardo_tribunal

usuario: ricardooropeza_tribunal 
contraseña: ricardooropeza_tribunal 

usuario: maria_tribunal
contraseña: maria_tribunal

usuario: antenas_fer123_tribunal
contraseña: antenas_fer123_tribunal

usuario: andresmujia_tribunal
contraseña: andresmujia_tribunal

usuario: romulo_roma_tribunal
contraseña: romulo_roma_tribunal 

```



# Instalación

Requisitos para la instalación en un entorno local:

* Sistema operativo con distribunación Linux (Para la ejecución del script de inicio).
* Python 3.8 o superior.

Clonar el repositorio y acceder en la carpeta etn1040_1/ para ejecutar el script de inicio.

    clone https://github.com/cesarcori/etn1040_1
    cd etn1040_1
    ./iniciar_configuracion.sh

Activar el entorno virtual

    source ../virtual-django/bin/activate 

Crear super usuario:

    python3 manage.py createsuperuser

Agregar docentes:

A través del inicio del sistema ingresar al URL: http://localhost:8000 con los datos: 

    Usuario: kardex
    Contraseña: kardex

En la pestaña **Docentes** Agregar mínimo un docente por mención. Por ejemplo:

    Nombre: Alberto
    Apellido: Ticona Callisaya
    Correo: albertoticona@gmail.com
    Grupo: A
    Mención: (Elegir opción)

El nombre del usuario y contraseña de los docentes, es generado por el sistema.
Toma como patrón la palabra antes del símbolo “@” del correo electrónico, 
seguido de la palabra “_docente”. 

Ejemplo 1: Correo: albertoticona@gmail.com

    Usuario: albertoticona_docente
    Contraseña: albertoticona_docente



