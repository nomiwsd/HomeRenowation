# Generated by Django 5.0 on 2024-05-01 14:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appsrc", "0022_bid_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="accepted",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="bid",
            name="declined",
            field=models.BooleanField(default=False),
        ),
    ]
