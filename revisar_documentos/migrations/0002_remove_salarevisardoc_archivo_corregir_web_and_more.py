# Generated by Django 4.0.2 on 2022-05-25 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('revisar_documentos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salarevisardoc',
            name='archivo_corregir_web',
        ),
        migrations.RemoveField(
            model_name='salarevisardoc',
            name='creado_por',
        ),
        migrations.AlterField(
            model_name='saladocumentodoc',
            name='tipo',
            field=models.CharField(choices=[('perfil', 'Perfil'), ('proyecto', 'Borrador de Proyecto'), ('tribunal', 'Proyecto Final Tribunal')], max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='SalaRevisarDocPredeterminado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=200, null=True)),
                ('detalle', models.TextField(blank=True, null=True)),
                ('archivo_corregir', models.FileField(blank=True, null=True, upload_to='material_estudiante_perfil/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('sala_documento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='revisar_documentos.saladocumentodoc')),
            ],
        ),
    ]
