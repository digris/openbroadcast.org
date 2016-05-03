# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid

def concat_uuid(apps, schema_editor):
    qs = apps.get_model("alibrary", "Label")
    for object in qs.objects.all():
        qs.objects.filter(pk=object.pk).update(uuid=object.uuid.replace('-', ''))


sql_uuid_migration = """
alter table alibrary_label alter column uuid type uuid using uuid::uuid;
"""

class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0019_auto_20160220_1719'),
    ]

    operations = [
        migrations.RunPython(concat_uuid),
        migrations.RunSQL(sql_uuid_migration, None, [
            migrations.AlterField(
                model_name='label',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
        ]),

    ]
