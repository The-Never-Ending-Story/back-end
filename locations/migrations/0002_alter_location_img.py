# Generated by Django 4.2.3 on 2023-07-14 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='img',
            field=models.TextField(default='none'),
        ),
    ]
