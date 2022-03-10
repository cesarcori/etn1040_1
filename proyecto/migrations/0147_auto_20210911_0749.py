# Generated by Django 3.2.6 on 2021-09-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0146_remove_datosestudiantetitulado_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datosestudiantetitulado',
            old_name='fecha_inscripcion',
            new_name='fecha_conclusion',
        ),
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('proyecto', 'Proyecto'), ('perfil', 'Perfil')], max_length=200, null=True),
        ),
    ]
