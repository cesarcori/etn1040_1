# Generated by Django 3.2.6 on 2021-10-14 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0165_auto_20210914_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('proyecto', 'Proyecto'), ('perfil', 'Perfil')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='solicitudinvitado',
            name='extension',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
