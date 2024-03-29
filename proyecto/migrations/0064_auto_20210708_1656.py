# Generated by Django 3.1.4 on 2021-07-08 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0063_auto_20210708_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialestudiante',
            name='docente_rev',
        ),
        migrations.RemoveField(
            model_name='materialestudiante',
            name='estudiante_rev',
        ),
        migrations.RemoveField(
            model_name='materialestudiante',
            name='tutor_rev',
        ),
        migrations.AddField(
            model_name='salarevisar',
            name='docente_rev',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.datosdocente'),
        ),
        migrations.AddField(
            model_name='salarevisar',
            name='estudiante_rev',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.datosestudiante'),
        ),
        migrations.AddField(
            model_name='salarevisar',
            name='tutor_rev',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.datostutor'),
        ),
    ]
