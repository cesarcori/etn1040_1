# Generated by Django 3.2.6 on 2021-08-29 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0117_datosestudiante_aceptar_tutoria'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datosestudiante',
            old_name='aceptar_tutoria',
            new_name='tutor_acepto',
        ),
    ]