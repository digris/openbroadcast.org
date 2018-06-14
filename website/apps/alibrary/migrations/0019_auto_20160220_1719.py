# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid

def concat_uuid(apps, schema_editor):

    qs = apps.get_model("alibrary", "Artist")
    for object in qs.objects.using(schema_editor.connection.alias).all():
        qs.objects.filter(pk=object.pk).update(uuid=object.uuid.replace('-', ''))

    return

def forwards(apps, schema_editor):
    if not schema_editor.connection.vendor == 'postgresql':
        print('db backend not postgres - skipping table update')
        return
    migrations.RunSQL(
        "alter table alibrary_artist alter column uuid type uuid using uuid::uuid;")

class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0018_delete_format'),
    ]

    operations = [
        migrations.RunPython(concat_uuid),
        migrations.RunPython(forwards, None, [
            migrations.AlterField(
                model_name='artist',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
        ]),
    ]
