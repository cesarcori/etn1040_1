# Generated by Django 4.0.2 on 2022-04-14 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensaje', '0039_mensajepar_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensaje',
            name='canal',
        ),
        migrations.RemoveField(
            model_name='mensaje',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='mensajepar',
            name='visto',
        ),
        migrations.AddField(
            model_name='mensajepar',
            name='is_visto',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Canal',
        ),
        migrations.DeleteModel(
            name='Mensaje',
        ),
    ]
