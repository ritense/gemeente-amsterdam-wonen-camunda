# Generated by Django 3.1.7 on 2021-03-10 18:00

from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("addresses", "0002_auto_20201028_0620"),
    ]

    operations = [
        TrigramExtension(),
    ]