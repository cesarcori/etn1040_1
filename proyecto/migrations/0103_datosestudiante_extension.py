# Generated by Django 3.2.6 on 2021-08-10 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0102_auto_20210806_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosestudiante',
            name='extension',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]