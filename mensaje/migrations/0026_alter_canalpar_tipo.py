# Generated by Django 4.0.2 on 2022-02-21 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensaje', '0025_alter_canalpar_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canalpar',
            name='tipo',
            field=models.CharField(choices=[('MENSAJE', 'MENSAJE'), ('OBSERVAR', 'OBSERVAR')], max_length=200, null=True),
        ),
    ]
