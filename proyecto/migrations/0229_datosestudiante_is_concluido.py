# Generated by Django 4.0.2 on 2022-06-22 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0228_datostribunal_menciones_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosestudiante',
            name='is_concluido',
            field=models.BooleanField(default=False),
        ),
    ]
