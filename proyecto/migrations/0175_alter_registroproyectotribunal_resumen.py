# Generated by Django 3.2.6 on 2021-12-08 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0174_alter_busquedaproyecto_perfil_proyecto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroproyectotribunal',
            name='resumen',
            field=models.TextField(null=True),
        ),
    ]