# Generated by Django 3.1.4 on 2021-07-07 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyecto', '0057_materialestudiante_texto'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorregirPerfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(blank=True, null=True)),
                ('material_para_corregir', models.FileField(null=True, upload_to='material_para_corregir/')),
                ('corregir_perfil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.materialestudiante')),
                ('docente_tutor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
