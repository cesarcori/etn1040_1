# Generated by Django 3.2.6 on 2021-09-04 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyecto', '0134_auto_20210904_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firma_carta_aceptacion', models.BooleanField(default=False)),
                ('firma_formulario1', models.BooleanField(default=False)),
                ('firma_carta_conclusion', models.BooleanField(default=False)),
                ('firma_formulario2', models.BooleanField(default=False)),
                ('firma_formulario3', models.BooleanField(default=False)),
                ('firma_formulario4', models.BooleanField(default=False)),
                ('usuario', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('proyecto', 'Proyecto'), ('perfil', 'Perfil')], max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Firmas',
        ),
    ]
