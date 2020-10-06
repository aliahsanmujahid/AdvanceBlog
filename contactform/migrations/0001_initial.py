# Generated by Django 2.2.8 on 2020-07-10 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('txt', models.TextField()),
                ('date', models.CharField(default='', max_length=12)),
                ('time', models.CharField(default='', max_length=12)),
            ],
        ),
    ]
