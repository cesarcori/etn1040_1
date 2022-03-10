# Generated by Django 3.2.6 on 2021-09-12 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0160_auto_20210912_0957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialdocente',
            name='visto',
        ),
        migrations.AddField(
            model_name='vistamaterialdocente',
            name='docente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.datosdocente'),
        ),
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('proyecto', 'Proyecto'), ('perfil', 'Perfil')], max_length=200, null=True),
        ),
    ]