# Generated by Django 3.1.4 on 2021-07-02 00:30

from django.db import migrations, models
import proyecto.models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0054_auto_20210701_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialdocente',
            name='material_docente',
            field=models.FileField(null=True, upload_to='material_docente/'),
        ),
        migrations.AlterField(
            model_name='reglamento',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='reglamentos/', validators=[proyecto.models.validate_file_extension]),
        ),
    ]