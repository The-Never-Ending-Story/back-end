# Generated by Django 4.2.3 on 2023-07-13 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worlds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='world',
            name='history',
            field=models.TextField(default='none'),
        ),
        migrations.AlterField(
            model_name='world',
            name='geodynamics',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='world',
            name='img',
            field=models.TextField(default='none'),
        ),
        migrations.AlterField(
            model_name='world',
            name='magictechnology',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='world',
            name='species',
            field=models.JSONField(default=dict),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('attributes', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('img', models.CharField(max_length=250)),
                ('type', models.CharField(default='none', max_length=250)),
                ('world_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worlds.world')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('time', models.TextField(default='none')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worlds.location')),
                ('world_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worlds.world')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('race', models.CharField(max_length=250)),
                ('alignment', models.CharField(max_length=250)),
                ('attributes', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('img', models.CharField(max_length=250)),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worlds.location')),
                ('world_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worlds.world')),
            ],
        ),
    ]
