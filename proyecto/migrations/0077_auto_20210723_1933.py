# Generated by Django 3.1.4 on 2021-07-23 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0076_auto_20210723_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroperfil',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.datosestudiante'),
        ),
    ]
