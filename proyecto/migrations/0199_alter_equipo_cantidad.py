# Generated by Django 4.0.2 on 2022-02-10 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0198_delete_solicitudmultiple'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='cantidad',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
