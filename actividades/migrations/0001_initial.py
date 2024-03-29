# Generated by Django 4.0.2 on 2022-02-08 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('valor', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('hecho', models.BooleanField(default=False)),
                ('fecha_inscripcion', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
