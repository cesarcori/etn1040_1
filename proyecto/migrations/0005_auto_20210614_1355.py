# Generated by Django 3.1.4 on 2021-06-14 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0004_datosdocente_mencion'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosestudiante',
            name='grupo',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='datosdocente',
            name='grupo',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]