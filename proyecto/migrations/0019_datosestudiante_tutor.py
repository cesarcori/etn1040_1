# Generated by Django 3.1.4 on 2021-06-15 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0018_auto_20210614_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosestudiante',
            name='tutor',
            field=models.ForeignKey(null=True, on_delete=models.SET(''), to='proyecto.datostutor'),
        ),
    ]
