# Generated by Django 4.0.2 on 2022-08-03 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0235_equipo_nivel_ie'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datosestudiante',
            options={'ordering': ['nivel_ie']},
        ),
        migrations.AlterModelOptions(
            name='equipo',
            options={'ordering': ['nivel_ie']},
        ),
        migrations.DeleteModel(
            name='MensajeSala',
        ),
        migrations.DeleteModel(
            name='Sala',
        ),
    ]