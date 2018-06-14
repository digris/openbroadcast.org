# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def forwards(apps, schema_editor):
    if not schema_editor.connection.vendor == 'postgresql':
        print('db backend not postgres - skipping table update')
    else:
        print('db backend is postgres - altering table')
        migrations.RunSQL("alter table alibrary_relation alter column object_id type integer using object_id::integer;")

class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0036_fix_fk_object_id'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop, [
            migrations.AlterField(
                model_name='relation',
                name='object_id',
                field=models.PositiveIntegerField(db_index=True),
            ),
        ]),
    ]
