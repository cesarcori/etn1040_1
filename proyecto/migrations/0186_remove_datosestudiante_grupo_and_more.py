# Generated by Django 4.0.2 on 2022-02-08 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0185_remove_grupoestudiante_integrantes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datosestudiante',
            name='grupo',
        ),
        migrations.AddField(
            model_name='datosestudiante',
            name='grupo_est',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.grupoestudiante'),
        ),
        migrations.AlterField(
            model_name='grupoestudiante',
            name='nombre',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
