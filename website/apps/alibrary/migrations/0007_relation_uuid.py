# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def populate_uuids(apps, schema_editor):
    Relation = apps.get_model("alibrary", "Relation")
    for r in Relation.objects.all():
        Relation.objects.filter(id=r.id).update(uuid=uuid.uuid4())


class Migration(migrations.Migration):

    dependencies = [
        ("alibrary", "0006_auto_20210308_2001"),
    ]

    operations = [
        migrations.AddField(
            model_name="relation",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                db_index=True,
            ),
        ),
        migrations.RunPython(populate_uuids),
    ]
