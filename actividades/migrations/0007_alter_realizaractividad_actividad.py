# Generated by Django 4.0.2 on 2022-02-12 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0006_alter_realizaractividad_estudiante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realizaractividad',
            name='actividad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.actividad'),
        ),
    ]
