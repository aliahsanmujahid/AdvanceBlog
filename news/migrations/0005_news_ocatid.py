# Generated by Django 2.2.8 on 2020-07-09 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_news_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='ocatid',
            field=models.IntegerField(default=0),
        ),
    ]
