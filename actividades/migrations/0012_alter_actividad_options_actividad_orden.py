# Generated by Django 4.0.2 on 2022-02-18 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0011_actividad_detalle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actividad',
            options={'ordering': ['-orden']},
        ),
        migrations.AddField(
            model_name='actividad',
            name='orden',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
