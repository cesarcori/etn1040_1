# Generated by Django 4.0.2 on 2022-06-07 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('revisar_documentos', '0011_salarevisardoc_is_calificado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saladocumentodoc',
            name='is_predeterminado',
        ),
        migrations.CreateModel(
            name='ConfiguracionSala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_predeterminado', models.BooleanField(default=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]