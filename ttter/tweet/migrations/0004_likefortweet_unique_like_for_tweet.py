# Generated by Django 4.0.2 on 2023-02-04 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0003_likefortweet'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='likefortweet',
            constraint=models.UniqueConstraint(fields=('user', 'tweet'), name='unique_like_for_tweet'),
        ),
    ]
