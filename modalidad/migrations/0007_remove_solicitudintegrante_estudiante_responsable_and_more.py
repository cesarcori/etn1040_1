# Generated by Django 4.0.2 on 2022-02-10 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0199_alter_equipo_cantidad'),
        ('modalidad', '0006_alter_rechazarsolicitud_detalle_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudintegrante',
            name='estudiante_responsable',
        ),
        migrations.AddField(
            model_name='solicitudintegrante',
            name='estudiante_interesado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interesado', to='proyecto.datosestudiante'),
        ),
    ]
