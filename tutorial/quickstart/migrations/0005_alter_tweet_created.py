# Generated by Django 3.2 on 2021-04-23 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0004_alter_tweet_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
