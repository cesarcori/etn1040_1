# Generated by Django 3.2.6 on 2021-08-27 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0112_alter_datosestudiante_imagen_perfil'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosadministrador',
            name='imagen_perfil',
            field=models.ImageField(default='imagenes/profile1.png', null=True, upload_to='imagenes/'),
        ),
        migrations.AddField(
            model_name='datosdocente',
            name='imagen_perfil',
            field=models.ImageField(default='imagenes/profile1.png', null=True, upload_to='imagenes/'),
        ),
        migrations.AddField(
            model_name='datostutor',
            name='imagen_perfil',
            field=models.ImageField(default='imagenes/profile1.png', null=True, upload_to='imagenes/'),
        ),
    ]
