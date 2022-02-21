# Generated by Django 4.0.2 on 2022-02-21 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0208_remove_progreso_usuario_progreso_equipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registroperfil',
            name='usuario',
        ),
        migrations.AddField(
            model_name='registroperfil',
            name='equipo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.equipo'),
        ),
    ]
