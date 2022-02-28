# Generated by Django 4.0.2 on 2022-02-28 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0213_remove_datosestudiante_solicitud_tribunal_docente_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registroproyectotribunal',
            name='usuario',
        ),
        migrations.AddField(
            model_name='registroproyectotribunal',
            name='equipo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.equipo'),
        ),
    ]
