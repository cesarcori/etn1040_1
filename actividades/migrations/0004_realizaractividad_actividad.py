# Generated by Django 4.0.2 on 2022-02-08 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0003_alter_actividad_options_remove_actividad_hecho_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='realizaractividad',
            name='actividad',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='actividades.actividad'),
        ),
    ]