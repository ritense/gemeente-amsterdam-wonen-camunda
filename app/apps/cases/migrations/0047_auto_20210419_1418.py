# Generated by Django 3.1.8 on 2021-04-19 12:18

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    def update_camunda_id_to_array(apps, schema_editor):
        Case = apps.get_model("cases", "Case")

        cases = Case.objects.all()

        for case in cases:
            case.camunda_id = "{" + case.camunda_id + "}"
            case.save()

    dependencies = [
        ("cases", "0046_auto_20210326_2028"),
    ]

    operations = [
        migrations.RunPython(update_camunda_id_to_array, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="case",
            name="camunda_id",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255),
                blank=True,
                null=True,
                size=None,
            ),
        ),
    ]
