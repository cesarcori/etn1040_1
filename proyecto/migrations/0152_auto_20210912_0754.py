# Generated by Django 3.2.6 on 2021-09-12 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0151_auto_20210912_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busquedaproyecto',
            name='perfil_proyecto',
            field=models.CharField(choices=[('perfil', 'Perfil'), ('proyecto', 'Proyecto')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='vistareglamento',
            name='reglamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.reglamento'),
        ),
        migrations.AlterField(
            model_name='vistareglamento',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.datosestudiante'),
        ),
    ]
