# Generated by Django 3.2.7 on 2021-10-08 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='watchlist',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='list', to='auctions.Listing'),
        ),
    ]
