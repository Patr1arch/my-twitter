# Generated by Django 3.2 on 2021-04-23 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0007_auto_20210423_0523'),
    ]

    operations = [
        migrations.AddField(
            model_name='followerfollows',
            name='follow_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
