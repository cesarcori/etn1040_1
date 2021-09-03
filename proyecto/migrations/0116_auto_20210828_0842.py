# Generated by Django 3.2.6 on 2021-08-28 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0115_auto_20210828_0837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datosestudiante',
            old_name='vb_perfil',
            new_name='vb_perfil_docente',
        ),
        migrations.RenameField(
            model_name='datosestudiante',
            old_name='vb_proyecto',
            new_name='vb_perfil_tutor',
        ),
        migrations.AddField(
            model_name='datosestudiante',
            name='vb_proyecto_docente',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='datosestudiante',
            name='vb_proyecto_tutor',
            field=models.BooleanField(default=False),
        ),
    ]