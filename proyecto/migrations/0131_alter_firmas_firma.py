# Generated by Django 3.2.6 on 2021-09-04 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0130_alter_firmas_firma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmas',
            name='firma',
            field=models.ImageField(default='firmas/firma_default.jpg', null=True, upload_to='firmas/'),
        ),
    ]