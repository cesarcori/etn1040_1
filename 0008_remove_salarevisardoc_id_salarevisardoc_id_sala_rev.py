# Generated by Django 4.0.2 on 2022-05-25 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revisar_documentos', '0007_saladocumentodoc_is_predeterminado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salarevisardoc',
            name='id',
        ),
        migrations.AddField(
            model_name='salarevisardoc',
            name='id_sala_rev',
            field=models.CharField(blank=True, max_length=10, primary_key=True, serialize=False),
        ),
    ]
