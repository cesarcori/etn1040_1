# Generated by Django 4.0.2 on 2022-03-04 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busquedas', '0002_proyectosinscritos_tutor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProyectosExcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.CharField(max_length=200, null=True)),
                ('titulo', models.CharField(max_length=200, null=True)),
                ('tutor', models.CharField(max_length=200, null=True)),
                ('docente', models.CharField(max_length=200, null=True)),
                ('resumen', models.TextField(blank=True, null=True)),
                ('indice', models.TextField(blank=True, null=True)),
                ('bibliografia', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('perfil', 'Perfil'), ('proyecto', 'Proyecto')], default='proyecto', max_length=200, null=True)),
                ('estado', models.CharField(choices=[('concluido', 'Concluido'), ('en proceso', 'En proceso')], default='concluido', max_length=200, null=True)),
                ('fecha_inicio', models.DateTimeField(blank=True, null=True)),
                ('fecha_concluida', models.DateTimeField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='proyectosinscritos',
            name='docente',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='proyectosinscritos',
            name='estado',
            field=models.CharField(choices=[('concluido', 'Concluido'), ('en proceso', 'En proceso')], default='concluido', max_length=200, null=True),
        ),
    ]
