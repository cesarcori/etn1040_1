# Generated by Django 3.2.6 on 2021-09-04 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0133_alter_busquedaproyecto_perfil_proyecto'),
    ]

    operations = [
        migrations.AddField(
            model_name='datostutor',
            name='firma',
            field=models.ImageField(default='firmas/firma_default.jpg', null=True, upload_to='firmas/'),
        ),
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('perfil', 'Perfil'), ('proyecto', 'Proyecto')], max_length=200, null=True),
        ),
    ]
