# Generated by Django 3.2.6 on 2022-01-12 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0175_alter_registroproyectotribunal_resumen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudinvitado',
            name='password',
        ),
        migrations.AlterField(
            model_name='comunicado',
            name='texto',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='proyectodegrado',
            name='resumen',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='registroperfil',
            name='resumen',
            field=models.TextField(null=True),
        ),
    ]
