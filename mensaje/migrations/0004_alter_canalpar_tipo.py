# Generated by Django 3.2.6 on 2022-01-12 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensaje', '0003_canalpar_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='canalpar',
            name='tipo',
            field=models.CharField(choices=[('MENSAJE', 'MENSAJE'), ('OBSERVAR', 'OBSERVAR')], max_length=200, null=True),
        ),
    ]
