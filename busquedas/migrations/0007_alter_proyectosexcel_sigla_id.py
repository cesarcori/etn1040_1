# Generated by Django 4.0.2 on 2022-03-05 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busquedas', '0006_alter_proyectosinscritos_sigla_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyectosexcel',
            name='sigla_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
