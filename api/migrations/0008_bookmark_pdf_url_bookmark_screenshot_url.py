# Generated by Django 4.2.3 on 2023-08-26 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_alter_tag_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookmark",
            name="pdf_url",
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="bookmark",
            name="screenshot_url",
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]