# Generated by Django 5.0 on 2024-03-26 17:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appsrc", "0003_user_profile_pic_workerprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_profile_set",
            field=models.BooleanField(default=False),
        ),
    ]
