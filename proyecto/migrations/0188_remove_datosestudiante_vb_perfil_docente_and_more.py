# Generated by Django 4.0.2 on 2022-02-08 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0187_alter_datosestudiante_grupo_est'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datosestudiante',
            name='vb_perfil_docente',
        ),
        migrations.RemoveField(
            model_name='datosestudiante',
            name='vb_perfil_tutor',
        ),
        migrations.RemoveField(
            model_name='datosestudiante',
            name='vb_proyecto_docente',
        ),
        migrations.RemoveField(
            model_name='datosestudiante',
            name='vb_proyecto_tutor',
        ),
        migrations.AlterField(
            model_name='datosestudiante',
            name='grupo_doc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='proyecto.datosdocente'),
        ),
        migrations.AlterField(
            model_name='datosestudiante',
            name='tutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proyecto.datostutor'),
        ),
        migrations.AlterField(
            model_name='grupoestudiante',
            name='perfil',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='proyecto.registroperfil'),
        ),
    ]
