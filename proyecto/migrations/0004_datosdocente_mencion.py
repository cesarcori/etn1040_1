# Generated by Django 3.1.4 on 2021-06-12 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0003_datosdocente_grupo'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosdocente',
            name='mencion',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
