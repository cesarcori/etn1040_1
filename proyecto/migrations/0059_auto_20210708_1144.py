# Generated by Django 3.1.4 on 2021-07-08 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0058_corregirperfil'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaCorreccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sala', models.CharField(max_length=50, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='corregirperfil',
            name='texto',
        ),
        migrations.AddField(
            model_name='corregirperfil',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='materialestudiante',
            name='sala_correccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.salacorreccion'),
        ),
    ]
