# Generated by Django 3.1.4 on 2021-06-14 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0010_auto_20210614_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatosAdministrador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=50, null=True, unique=True)),
                ('correo', models.CharField(max_length=50, null=True, unique=True)),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('apellido', models.CharField(max_length=50, null=True)),
                ('celular', models.CharField(max_length=50, null=True)),
                ('fecha_inscripcion', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='datosdocente',
            old_name='fecha_solicitud',
            new_name='fecha_inscripcion',
        ),
        migrations.RenameField(
            model_name='datostutor',
            old_name='fecha_solicitud',
            new_name='fecha_inscripcion',
        ),
    ]