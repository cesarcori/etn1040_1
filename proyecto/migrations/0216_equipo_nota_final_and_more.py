# Generated by Django 4.0.2 on 2022-02-28 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0215_remove_registroproyectotribunal_nota_final_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo',
            name='nota_final',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registroproyectotribunal',
            name='nota',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
