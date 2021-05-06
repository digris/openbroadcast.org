# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from cacheops import invalidate_model


def forwards_func(apps, schema_editor):
    PreflightCheck = apps.get_model("media_preflight", "PreflightCheck")

    for preflight_check in PreflightCheck.objects.all().select_related("media"):
        print("migrating pfc", preflight_check.id)

        if not preflight_check.result:
            continue

        try:
            old_checks = preflight_check.result.get("checks", {})
            old_errors = preflight_check.result.get("errors", {})
        except AttributeError:
            continue

        checks = {
            "decode_file": old_checks.get("decode", None) == "ok",
            "read_decoded_file": old_checks.get("out_file", None) == "ok",
            "decoded_duration": old_checks.get("duration_preflight", None),
        }

        warnings = []
        errors = old_errors.values()

        try:
            decoded_duration = checks.get("decoded_duration", None)
            master_duration = preflight_check.media.master_duration

            if decoded_duration and master_duration:
                diff = abs(decoded_duration - master_duration)
                if diff > 5.0:
                    errors.append(
                        "duration mismatch: {:.2f}s".format(diff),
                    )
                elif diff > 2.0:
                    warnings.append(
                        "duration mismatch: {:.2f}s".format(diff),
                    )
        except:
            print("unable to check durations")

        preflight_check.checks = checks
        preflight_check.warnings = warnings
        preflight_check.errors = errors

        preflight_check.save()

    # remove old / unformatted duration error
    for preflight_check in PreflightCheck.objects.filter(
        errors__icontains="duration mismatch - master"
    ):
        preflight_check.errors = [
            e
            for e in preflight_check.errors
            if not e.startswith("duration mismatch - master")
        ]
        preflight_check.save()

    # set 'hanging' checks to complete
    PreflightCheck.objects.filter(status__in=["pending", "running"]).update(
        status="completed",
        warnings=["check timed out"],
    )

    invalidate_model(PreflightCheck)


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("media_preflight", "0005_auto_20210506_1020"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
