# Generated by Django 3.1.4 on 2021-07-08 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0067_salarevisar_material_estudiante'),
    ]

    operations = [
        migrations.AddField(
            model_name='salarevisar',
            name='texto',
            field=models.TextField(blank=True, null=True),
        ),
    ]
