# Generated by Django 3.0.8 on 2020-07-10 04:08

import uuid

from django.db import migrations


def create_uuid(apps, schema_editor):
    User = apps.get_model("users", "User")
    for user in User.objects.all():
        user.id = uuid.uuid4()
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_uuid),
    ]
