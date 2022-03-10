# Generated by Django 4.0.2 on 2022-02-16 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0204_equipo_docente'),
        ('revisar', '0006_alter_saladocumentoapp_tipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saladocumentoapp',
            name='estudiante',
        ),
        migrations.AddField(
            model_name='saladocumentoapp',
            name='equipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.equipo'),
        ),
    ]