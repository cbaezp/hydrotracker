# Generated by Django 4.2.7 on 2023-11-05 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("plants", "0002_remove_plant_datetime_stage_updated_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plant",
            name="plant_info",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="plants.plantinfo"),
        ),
    ]