# Generated by Django 3.1.4 on 2021-07-27 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0084_auto_20210726_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrocronograma',
            name='semana',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
