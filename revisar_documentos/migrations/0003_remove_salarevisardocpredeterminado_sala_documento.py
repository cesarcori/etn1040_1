# Generated by Django 4.0.2 on 2022-05-25 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revisar_documentos', '0002_remove_salarevisardoc_archivo_corregir_web_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salarevisardocpredeterminado',
            name='sala_documento',
        ),
    ]
