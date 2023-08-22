# Generated by Django 4.2.3 on 2023-08-22 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worlds', '0005_world_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='world',
            name='hero',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='world',
            name='heros',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='world',
            name='thumbnail',
            field=models.TextField(default=''),
        ),
    ]
