# Generated by Django 3.2.6 on 2021-09-12 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0157_auto_20210912_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('perfil', 'Perfil'), ('proyecto', 'Proyecto')], max_length=200, null=True),
        ),
    ]
