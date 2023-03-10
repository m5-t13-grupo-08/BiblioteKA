# Generated by Django 4.1.7 on 2023-03-07 19:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("books", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="followed_by",
            field=models.ManyToManyField(
                related_name="followed_books", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
