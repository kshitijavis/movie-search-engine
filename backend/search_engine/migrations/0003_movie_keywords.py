# Generated by Django 3.2.5 on 2021-07-25 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0002_auto_20210725_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='keywords',
            field=models.ManyToManyField(related_name='movies', to='search_engine.Keyword'),
        ),
    ]
