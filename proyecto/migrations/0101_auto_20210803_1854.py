# Generated by Django 3.1.4 on 2021-08-03 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0100_proyectodegrado_calificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyectodegrado',
            name='calificacion',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
