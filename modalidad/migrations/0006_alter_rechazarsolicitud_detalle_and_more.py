# Generated by Django 4.0.2 on 2022-02-10 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0199_alter_equipo_cantidad'),
        ('modalidad', '0005_alter_solicitud_estudiante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rechazarsolicitud',
            name='detalle',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='detalle',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='SolicitudIntegrante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visto', models.BooleanField(default=False)),
                ('aprobar', models.BooleanField(default=False)),
                ('rechazar', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('estudiante_invitado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitado', to='proyecto.datosestudiante')),
                ('estudiante_responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsable', to='proyecto.datosestudiante')),
            ],
        ),
    ]