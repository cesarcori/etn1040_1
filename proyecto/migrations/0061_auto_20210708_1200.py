# Generated by Django 3.1.4 on 2021-07-08 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0060_auto_20210708_1146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='materialestudiante',
            old_name='sala_correccion',
            new_name='sala_revisar',
        ),
    ]