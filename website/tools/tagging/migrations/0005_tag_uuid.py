# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def populate_uuids(apps, schema_editor):
    Tag = apps.get_model("tagging", "Tag")
    for t in Tag.objects.all():
        Tag.objects.filter(id=t.id).update(uuid=uuid.uuid4())


class Migration(migrations.Migration):

    dependencies = [
        ("tagging", "0004_auto_20200115_1017"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                db_index=True,
            ),
        ),
        migrations.RunPython(populate_uuids),
    ]
