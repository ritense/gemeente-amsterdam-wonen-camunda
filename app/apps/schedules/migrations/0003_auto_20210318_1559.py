# Generated by Django 3.1.7 on 2021-03-18 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0042_auto_20210224_2009"),
        ("schedules", "0002_default_values"),
    ]

    operations = [
        migrations.AlterField(
            model_name="daysegment",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="day_segments",
                to="cases.caseteam",
            ),
        ),
        migrations.AlterField(
            model_name="priority",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="priorities",
                to="cases.caseteam",
            ),
        ),
        migrations.AlterField(
            model_name="weeksegment",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="week_segments",
                to="cases.caseteam",
            ),
        ),
        migrations.CreateModel(
            name="Action",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="actions",
                        to="cases.caseteam",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "unique_together": {("name", "team")},
            },
        ),
        migrations.AlterField(
            model_name="schedule",
            name="schedule_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="schedules.action"
            ),
        ),
        migrations.DeleteModel(
            name="ScheduleType",
        ),
    ]
