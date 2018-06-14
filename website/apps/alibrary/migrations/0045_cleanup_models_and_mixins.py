# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-06-09 16:34
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def forwards(apps, schema_editor):
    print('CONNECTION TYPE: {}'.format(schema_editor.connection.vendor))


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0044_cleanup_distributor'),
    ]

    operations = [
        migrations.RunPython(forwards, None, [
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
                field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
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
                field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
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
                field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
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
                field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
            ),
            # migrations.AlterField(
            #     model_name='profession',
            #     name='created',
            #     field=models.DateTimeField(auto_now_add=True, db_index=True),
            # ),
            # migrations.AlterField(
            #     model_name='profession',
            #     name='updated',
            #     field=models.DateTimeField(auto_now=True, db_index=True),
            # ),
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
                field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
            ),
        ]),
    ]
