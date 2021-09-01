# Generated by Django 3.2.6 on 2021-08-31 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0119_busquedaproyecto'),
    ]

    operations = [
        migrations.AddField(
            model_name='busquedaproyecto',
            name='bibliografia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='busquedaproyecto',
            name='indice',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('proyecto', 'Proyecto'), ('perfil', 'Perfil')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='busquedaproyecto',
            name='resumen',
            field=models.TextField(blank=True, null=True),
        ),
    ]
