# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from cacheops import invalidate_model


def forwards_func(apps, schema_editor):
    PreflightCheck = apps.get_model("media_preflight", "PreflightCheck")

    PreflightCheck.objects.filter(status="0").update(status="pending")
    PreflightCheck.objects.filter(status="1").update(status="running")
    PreflightCheck.objects.filter(status="2").update(status="completed")
    PreflightCheck.objects.filter(status="99").update(status="error")

    invalidate_model(PreflightCheck)


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("media_preflight", "0004_auto_20210505_1903"),
    ]

    operations = [
        migrations.AlterField(
            model_name="preflightcheck",
            name="status",
            field=models.CharField(
                default="pending",
                max_length=16,
                verbose_name="Status",
                db_index=True,
                choices=[
                    ("pending", "Pending"),
                    ("running", "Running"),
                    ("completed", "Completed"),
                    ("error", "Error"),
                ],
            ),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
