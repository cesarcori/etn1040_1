# Generated by Django 3.1.4 on 2021-06-30 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0042_auto_20210630_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datosdocente',
            name='material_docente',
        ),
        migrations.CreateModel(
            name='MaterialDocente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_docente', models.FileField(blank=True, null=True, upload_to='material_docente/')),
                ('propietario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.datosdocente')),
            ],
        ),
    ]