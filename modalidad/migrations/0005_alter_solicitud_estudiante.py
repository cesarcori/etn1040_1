# Generated by Django 4.0.2 on 2022-02-10 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0198_delete_solicitudmultiple'),
        ('modalidad', '0004_rename_rechazosolicitud_rechazarsolicitud'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='estudiante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.datosestudiante'),
        ),
    ]