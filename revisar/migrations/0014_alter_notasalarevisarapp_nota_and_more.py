# Generated by Django 4.0.2 on 2022-05-10 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revisar', '0013_notasalarevisarapp_nota_max_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notasalarevisarapp',
            name='nota',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='notasalarevisarapp',
            name='nota_max',
            field=models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=3, null=True),
        ),
    ]
