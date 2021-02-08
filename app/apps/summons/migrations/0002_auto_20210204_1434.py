# Generated by Django 3.1.5 on 2021-02-04 13:34

from apps.summons.const import SUMMON_TYPES
from django.conf import settings
from django.db import migrations


def add_summon_types(apps, schema_editor):
    SummonType = apps.get_model("summons", "SummonType")
    CaseTeam = apps.get_model("cases", "CaseTeam")
    default_case_team, _ = CaseTeam.objects.get_or_create(name=settings.DEFAULT_TEAM)

    for summon_type in SUMMON_TYPES:
        SummonType.objects.get_or_create(name=summon_type, team=default_case_team)


class Migration(migrations.Migration):

    dependencies = [
        ("summons", "0001_initial"),
    ]

    operations = [migrations.RunPython(add_summon_types)]