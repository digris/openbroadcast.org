# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards(apps, schema_editor):
    if not schema_editor.connection.vendor == 'postgresql':
        print('db backend not postgres - skipping table update')
        return
    else:
        print('db backend is postgres - skipping table update')
    migrations.RunSQL(
        "alter table alibrary_artist alter column uuid type uuid using uuid::uuid;")


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0026_relation_db_index'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='licensetranslation',
            options={'default_permissions': (), 'managed': True},
        ),
        migrations.RemoveField(
            model_name='artist',
            name='enable_comments',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='summary',
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='enable_comments',
        ),
        migrations.RemoveField(
            model_name='release',
            name='enable_comments',
        ),
        migrations.AlterField(
            model_name='artist',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
