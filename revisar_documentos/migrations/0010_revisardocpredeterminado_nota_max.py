# Generated by Django 4.0.2 on 2022-05-29 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revisar_documentos', '0009_revisardocpersonalizado_nota_max'),
    ]

    operations = [
        migrations.AddField(
            model_name='revisardocpredeterminado',
            name='nota_max',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=3, null=True),
        ),
    ]
