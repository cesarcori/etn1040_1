# Generated by Django 4.0.2 on 2022-02-18 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0204_equipo_docente'),
        ('revisar', '0007_remove_saladocumentoapp_estudiante_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salarevisarapp',
            name='creado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.datosestudiante'),
        ),
    ]
