# Generated by Django 3.1.4 on 2021-07-27 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0088_auto_20210726_2226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registrocronograma',
            old_name='semana',
            new_name='semana_final',
        ),
        migrations.AddField(
            model_name='registrocronograma',
            name='semana_inicial',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
