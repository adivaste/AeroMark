# Generated by Django 4.2.3 on 2023-08-15 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookmark",
            name="thumbnail_url",
            field=models.URLField(
                blank=True,
                default="https://i.ibb.co/3RLm4Jc/629a49e7ab53625cb2c4e791-Brand-pattern.jpg",
            ),
        ),
    ]
