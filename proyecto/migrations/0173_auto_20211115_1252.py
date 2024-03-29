# Generated by Django 3.2.6 on 2021-11-15 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0172_registroproyectotribunal'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroproyectotribunal',
            name='nota_final',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('proyecto', 'Proyecto'), ('perfil', 'Perfil')], max_length=200, null=True),
        ),
    ]
