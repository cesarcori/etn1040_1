# Generated by Django 4.0.2 on 2022-05-12 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tituloperfil',
            name='titulo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
