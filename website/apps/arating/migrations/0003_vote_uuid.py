# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def populate_uuids(apps, schema_editor):
    Vote = apps.get_model("arating", "Vote")
    for r in Vote.objects.all():
        Vote.objects.filter(id=r.id).update(uuid=uuid.uuid4())


class Migration(migrations.Migration):

    dependencies = [
        ("arating", "0002_auto_20180910_1308"),
    ]

    operations = [
        migrations.AddField(
            model_name="vote",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                db_index=True,
            ),
        ),
        migrations.RunPython(populate_uuids),
    ]
