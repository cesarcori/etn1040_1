# Generated by Django 3.1.4 on 2021-06-28 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0033_auto_20210623_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosdocente',
            name='nombre_sala_estudiante',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='datosestudiante',
            name='nombre_sala_docente',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='datosestudiante',
            name='nombre_sala_tutor',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='datostutor',
            name='nombre_sala_estudiante',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
