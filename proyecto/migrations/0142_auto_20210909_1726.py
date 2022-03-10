# Generated by Django 3.2.6 on 2021-09-09 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0141_auto_20210909_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auspicio',
            name='cargo',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='auspicio',
            name='empresa',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='auspicio',
            name='supervisor',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('perfil', 'Perfil'), ('proyecto', 'Proyecto')], max_length=200, null=True),
        ),
    ]
