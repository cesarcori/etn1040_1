# Generated by Django 3.2.6 on 2022-01-12 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyecto', '0178_alter_solicitudinvitado_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudinvitado',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
