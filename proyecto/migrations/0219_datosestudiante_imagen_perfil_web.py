# Generated by Django 4.0.2 on 2022-03-05 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0218_delete_busquedaproyecto'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosestudiante',
            name='imagen_perfil_web',
            field=models.URLField(null=True),
        ),
    ]