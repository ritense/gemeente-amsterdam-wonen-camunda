# Generated by Django 3.1.2 on 2020-10-29 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_remove_event_values"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="type",
            field=models.CharField(
                choices=[("DEBRIEFING", "DEBRIEFING")], max_length=250
            ),
        ),
    ]
