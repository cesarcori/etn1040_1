# Generated by Django 4.0.2 on 2022-02-22 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0211_remove_datosestudiante_tribunales_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='alias',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
