# Generated by Django 3.1.4 on 2021-06-14 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyecto', '0014_auto_20210614_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosdocente',
            name='usuario2',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='datosdocente',
            name='usuario',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
