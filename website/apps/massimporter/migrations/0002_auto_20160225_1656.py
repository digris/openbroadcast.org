# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def forwards(apps, schema_editor):
    if not schema_editor.connection.vendor == 'postgresql':
        print('db backend not postgres - skipping table update')
        return
    migrations.RunSQL("""alter table massimporter_massimport alter column uuid type uuid using uuid::uuid;
alter table massimporter_massimportfile alter column uuid type uuid using uuid::uuid;""")

class Migration(migrations.Migration):

    dependencies = [
        ('massimporter', '0001_initial'),
    ]

    operations = [

        migrations.RunPython(forwards, None, [
            migrations.AlterField(
                model_name='massimport',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4),
            ),
            migrations.AlterField(
                model_name='massimportfile',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4),
            ),
        ]),

    ]
