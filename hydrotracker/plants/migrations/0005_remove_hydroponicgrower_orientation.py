# Generated by Django 4.2.7 on 2023-11-07 02:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("plants", "0004_plant_creation_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hydroponicgrower",
            name="orientation",
        ),
    ]
