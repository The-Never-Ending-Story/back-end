# Generated by Django 4.2.3 on 2023-07-16 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='imgs',
            field=models.TextField(default=list),
        ),
    ]
