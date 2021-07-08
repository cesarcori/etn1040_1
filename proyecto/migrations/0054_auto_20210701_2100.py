# Generated by Django 3.1.4 on 2021-07-01 21:00

from django.db import migrations, models
import proyecto.models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0053_auto_20210701_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialdocente',
            name='material_docente',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='reglamento',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[proyecto.models.validate_file_extension]),
        ),
    ]