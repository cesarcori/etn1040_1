# Generated by Django 4.0.2 on 2022-02-18 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0010_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='detalle',
            field=models.TextField(blank=True, null=True),
        ),
    ]