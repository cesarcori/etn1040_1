# Generated by Django 4.0.2 on 2022-03-04 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProyectosInscritos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autor', models.CharField(max_length=200, null=True)),
                ('titulo', models.CharField(max_length=200, null=True)),
                ('resumen', models.TextField(blank=True, null=True)),
                ('indice', models.TextField(blank=True, null=True)),
                ('bibliografia', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('perfil', 'Perfil'), ('proyecto', 'Proyecto')], max_length=200, null=True)),
                ('estado', models.CharField(choices=[('concluido', 'Concluido'), ('en proceso', 'En proceso')], max_length=200, null=True)),
                ('fecha_inicio', models.DateTimeField(null=True)),
                ('fecha_concluida', models.DateTimeField(null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
