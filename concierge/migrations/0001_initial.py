# Generated by Django 2.2 on 2019-06-15 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('url', models.CharField(max_length=128)),
                ('saved_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('prefecture', models.CharField(blank=True, max_length=64, null=True)),
                ('region', models.CharField(blank=True, max_length=64, null=True)),
                ('district', models.CharField(blank=True, max_length=64, null=True)),
                ('station', models.CharField(blank=True, max_length=64, null=True)),
                ('level', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=128)),
                ('genre_name', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
                ('url', models.CharField(max_length=128)),
                ('img_url', models.CharField(max_length=256)),
                ('rank', models.IntegerField()),
                ('rate', models.FloatField()),
                ('is_day', models.BooleanField()),
                ('saved_date', models.DateTimeField()),
            ],
        ),
    ]
