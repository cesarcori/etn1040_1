# Generated by Django 4.0.2 on 2022-06-23 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0229_datosestudiante_is_concluido'),
        ('actividades', '0015_remove_avisoactividad_cantidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActividadHistorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('actividad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.actividad')),
                ('equipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.equipo')),
            ],
        ),
    ]