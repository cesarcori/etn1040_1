# Generated by Django 3.1.4 on 2021-07-31 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0096_auto_20210731_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialestudiante',
            name='sala',
        ),
        migrations.RemoveField(
            model_name='materialestudianteproyecto',
            name='sala',
        ),
        migrations.AlterField(
            model_name='salarevisar',
            name='material_estudiante',
            field=models.FileField(null=True, upload_to='material_estudiante_perfil/'),
        ),
        migrations.AlterField(
            model_name='salarevisarproyecto',
            name='material_estudiante',
            field=models.FileField(null=True, upload_to='material_estudiante_proyecto/'),
        ),
        migrations.DeleteModel(
            name='CorregirPerfil',
        ),
        migrations.DeleteModel(
            name='MaterialEstudiante',
        ),
        migrations.DeleteModel(
            name='MaterialEstudianteProyecto',
        ),
    ]