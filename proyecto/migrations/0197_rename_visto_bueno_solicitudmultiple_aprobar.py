# Generated by Django 4.0.2 on 2022-02-09 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0196_solicitudmultiple_visto_bueno'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitudmultiple',
            old_name='visto_bueno',
            new_name='aprobar',
        ),
    ]
