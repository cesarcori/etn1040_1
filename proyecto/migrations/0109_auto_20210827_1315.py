# Generated by Django 3.2.6 on 2021-08-27 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0108_rename_profile_pic_datosestudiante_imagen_perfil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datosestudiante',
            name='cronograma',
        ),
        migrations.AlterField(
            model_name='datosestudiante',
            name='tutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(''), to='proyecto.datostutor'),
        ),
    ]