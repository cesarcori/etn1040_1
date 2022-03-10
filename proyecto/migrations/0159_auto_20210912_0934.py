# Generated by Django 3.2.6 on 2021-09-12 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0158_alter_busquedaproyecto_perfil_proyecto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vistareglamento',
            old_name='reglamento',
            new_name='reglamento_visto',
        ),
        migrations.RemoveField(
            model_name='vistareglamento',
            name='visto',
        ),
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('proyecto', 'Proyecto'), ('perfil', 'Perfil')], max_length=200, null=True),
        ),
    ]
