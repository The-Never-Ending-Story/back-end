# Generated by Django 4.2.3 on 2023-07-08 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worlds', '0005_alter_world_magictechnology'),
    ]

    operations = [
        migrations.AlterField(
            model_name='world',
            name='magictechnology',
            field=models.TextField(),
        ),
    ]
