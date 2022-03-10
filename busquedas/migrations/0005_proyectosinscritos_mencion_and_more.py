# Generated by Django 4.0.2 on 2022-03-05 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busquedas', '0004_proyectosexcel_mencion_proyectosexcel_sigla_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyectosinscritos',
            name='mencion',
            field=models.CharField(choices=[('telecomunicacion', 'Telecomunicación'), ('control', 'Control'), ('sistemas', 'Sistemas de Computación')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='proyectosinscritos',
            name='sigla_id',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='proyectosinscritos',
            name='tesistas',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='proyectosexcel',
            name='sigla_id',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
