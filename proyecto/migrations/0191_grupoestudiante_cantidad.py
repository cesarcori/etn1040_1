# Generated by Django 4.0.2 on 2022-02-08 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0190_remove_grupoestudiante_perfil_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupoestudiante',
            name='cantidad',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]