# Generated by Django 3.1.4 on 2021-06-20 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('proyecto', '0022_auto_20210620_0401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensajepersonal',
            name='autor2',
        ),
        migrations.AlterField(
            model_name='mensajepersonal',
            name='destino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
        ),
    ]