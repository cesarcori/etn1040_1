# Generated by Django 3.2.6 on 2021-11-19 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0173_auto_20211115_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('perfil', 'Perfil'), ('proyecto', 'Proyecto')], max_length=200, null=True),
        ),
    ]
