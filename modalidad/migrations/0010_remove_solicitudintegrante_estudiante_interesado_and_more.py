# Generated by Django 4.0.2 on 2022-02-15 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0202_delete_actividad_alter_datosestudiante_actividad'),
        ('modalidad', '0009_alter_solicitudintegrante_correo_invitado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudintegrante',
            name='estudiante_interesado',
        ),
        migrations.AddField(
            model_name='solicitudintegrante',
            name='equipo_interesado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interesado', to='proyecto.equipo'),
        ),
    ]