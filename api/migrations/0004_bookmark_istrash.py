# Generated by Django 4.2.3 on 2023-08-16 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_bookmark_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookmark",
            name="isTrash",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
