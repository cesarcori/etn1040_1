# Generated by Django 4.0.2 on 2022-06-28 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0233_alter_datosestudiante_nivel_ie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosestudiante',
            name='nivel_ie',
            field=models.DecimalField(blank=True, decimal_places=5, default=0, max_digits=10, null=True),
        ),
    ]
