# Generated by Django 2.2.8 on 2020-07-06 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='catid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='news',
            name='catname',
            field=models.CharField(default='-', max_length=34),
        ),
        migrations.AddField(
            model_name='news',
            name='show',
            field=models.IntegerField(default=0),
        ),
    ]
