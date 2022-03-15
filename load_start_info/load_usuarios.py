#!/usr/bin/env python3 
from django.contrib.auth.models import User, Group
from proyecto.models import DatosAdministrador, DatosDirector

# para ejecutar este script dentro de shell ejecutar el siguiente comando en
# la terminal, dentro del proyecto.
# python manage.py shell -i python < load_db.py
# otra forma de poblar datos es mediante dumpdata y fixtures
if User.objects.filter(username='kardex').exists() and User.objects.filter(username='director').exists():
    print("*** Ya se cargo los usuarios iniciales")
else: 
    admi = Group.objects.get(name='administrador')
    director = Group.objects.get(name='director')
# creacion del superadministrdor:
    usuarios = [
        {'usuario':'kardex',
        'password':'kardex',
        'correo':'kardex@gmail.com',
        'grupo': admi },
        {'usuario':'director',
        'password':'director',
        'correo':'director@gmail.com',
        'grupo': director},
        ]
    for u in usuarios:
        User.objects.create_user(username=u['usuario'], password=u['password'], email=u['correo'])
        actor = User.objects.get(username=u['usuario'])
        actor.groups.add(u['grupo'])
        actor.save()
        # create datos
        if u['grupo'].name == 'administrador':
            DatosAdministrador.objects.create(
                usuario = actor,
                correo = u['correo']
                )
        elif u['grupo'].name == 'director':
            DatosDirector.objects.create(
                usuario = actor,
                correo = u['correo']
                )


    


