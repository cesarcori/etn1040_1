# Generated by Django 4.0.2 on 2022-02-08 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0186_remove_datosestudiante_grupo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosestudiante',
            name='grupo_est',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proyecto.grupoestudiante'),
        ),
    ]