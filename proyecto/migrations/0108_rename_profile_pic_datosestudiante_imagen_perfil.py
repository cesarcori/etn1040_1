# Generated by Django 3.2.6 on 2021-08-27 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0107_alter_datosestudiante_extension'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datosestudiante',
            old_name='profile_pic',
            new_name='imagen_perfil',
        ),
    ]
