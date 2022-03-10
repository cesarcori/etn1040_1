# Generated by Django 3.2.6 on 2021-09-09 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0138_auto_20210908_1927'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UrlPrincipal',
        ),
        migrations.AddField(
            model_name='salarevisar',
            name='material_corregido_docente',
            field=models.FileField(null=True, upload_to='material_estudiante_perfil/'),
        ),
        migrations.AddField(
            model_name='salarevisar',
            name='material_corregido_tutor',
            field=models.FileField(null=True, upload_to='material_estudiante_perfil/'),
        ),
    ]