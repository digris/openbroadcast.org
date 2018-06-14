# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid

def forwards(apps, schema_editor):
    if not schema_editor.connection.vendor == 'postgresql':
        print('db backend not postgres - skipping table update')
        return
    else:
        print('db backend is postgres - run type updates')

        sql_lines = [
            'ALTER TABLE alibrary_distributor ALTER COLUMN uuid type uuid USING uuid::uuid;',
            'ALTER TABLE alibrary_media ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE alibrary_playlist ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE alibrary_playlistitem ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE alibrary_playlistitemplaylist ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE alibrary_release ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE alibrary_series ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE abcast_channel ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE abcast_emission ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE abcast_jingle ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE abcast_onairitem ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE abcast_station ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE alibrary_relation ALTER COLUMN object_id type INTEGER USING object_id::integer;'
            'ALTER TABLE alibrary_label ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE alibrary_artist ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE massimporter_massimport ALTER COLUMN uuid type uuid USING uuid::uuid;'
            'ALTER TABLE massimporter_massimportfile ALTER COLUMN uuid type uuid USING uuid::uuid;'
        ]

        for line in sql_lines:
            print('SQL: {}'.format(line))
            migrations.RunSQL(line)

class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0045_cleanup_models_and_mixins'),
    ]

    operations = [
        migrations.RunPython(forwards, None, [
            migrations.RemoveField(
                model_name='profession',
                name='created',
            ),
            migrations.RemoveField(
                model_name='profession',
                name='updated',
            ),
            migrations.AlterField(
                model_name='artist',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
            migrations.AlterField(
                model_name='distributor',
                name='created',
                field=models.DateTimeField(auto_now_add=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='distributor',
                name='updated',
                field=models.DateTimeField(auto_now=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='distributor',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
            ),
            migrations.AlterField(
                model_name='label',
                name='created',
                field=models.DateTimeField(auto_now_add=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='label',
                name='updated',
                field=models.DateTimeField(auto_now=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='label',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
            ),
            migrations.AlterField(
                model_name='license',
                name='created',
                field=models.DateTimeField(auto_now_add=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='license',
                name='updated',
                field=models.DateTimeField(auto_now=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='license',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
            ),
            migrations.AlterField(
                model_name='media',
                name='created',
                field=models.DateTimeField(auto_now_add=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='media',
                name='updated',
                field=models.DateTimeField(auto_now=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='media',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
            ),
            migrations.AlterField(
                model_name='playlist',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
            migrations.AlterField(
                model_name='playlistitem',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
            migrations.AlterField(
                model_name='playlistitemplaylist',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
            migrations.AlterField(
                model_name='relation',
                name='created',
                field=models.DateTimeField(auto_now_add=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='relation',
                name='updated',
                field=models.DateTimeField(auto_now=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='release',
                name='created',
                field=models.DateTimeField(auto_now_add=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='release',
                name='updated',
                field=models.DateTimeField(auto_now=True, db_index=True),
            ),
            migrations.AlterField(
                model_name='release',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
            ),
            migrations.AlterField(
                model_name='series',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
        ]),
    ]
