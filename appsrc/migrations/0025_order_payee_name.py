# Generated by Django 5.0 on 2024-05-01 15:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appsrc", "0024_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="payee_name",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
