# Generated by Django 3.1.7 on 2021-03-24 19:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("visits", "0006_auto_20210324_2023"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visit",
            name="observations",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255),
                blank=True,
                null=True,
                size=None,
            ),
        ),
    ]
