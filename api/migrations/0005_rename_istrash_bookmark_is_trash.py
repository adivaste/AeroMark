# Generated by Django 4.2.3 on 2023-08-16 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_bookmark_istrash"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bookmark",
            old_name="isTrash",
            new_name="is_trash",
        ),
    ]
