# Generated by Django 4.0.2 on 2022-02-08 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0191_grupoestudiante_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosestudiante',
            name='tribunales',
            field=models.ManyToManyField(blank=True, to='proyecto.DatosTribunal'),
        ),
    ]
