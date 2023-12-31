# Generated by Django 4.2.7 on 2023-11-05 01:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("plants", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plant",
            name="datetime_stage_updated",
        ),
        migrations.AddField(
            model_name="plant",
            name="datetime_germination_to_growing",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="plant",
            name="datetime_growing_to_cropped",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
