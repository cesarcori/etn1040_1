# Generated by Django 3.2.6 on 2021-09-10 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0143_auto_20210910_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('perfil', 'Perfil'), ('proyecto', 'Proyecto')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='datosdirector',
            name='apellido',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='datosdirector',
            name='celular',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='datosdirector',
            name='correo',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='datosdirector',
            name='nombre',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
