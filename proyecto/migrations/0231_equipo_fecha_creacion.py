# Generated by Django 4.0.2 on 2022-06-28 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0230_datosestudiante_nivel_ie'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
