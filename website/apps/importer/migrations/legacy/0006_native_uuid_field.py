# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import importer.models
import uuid
import django_extensions.db.fields.json


def concat_uuids(apps, schema_editor):

    items = [
        'Import',
        'ImportFile',
        'ImportItem',
    ]

    for item in items:
        qs = apps.get_model("importer", item)
        print('concat uuids on {}'.format(item))
        for obj in qs.objects.using(schema_editor.connection.alias).all():
            qs.objects.filter(pk=obj.pk).update(uuid=obj.uuid.replace('-', ''))


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0005_import_collection_name'),
    ]

    operations = [

        migrations.RunPython(concat_uuids),

        migrations.AlterField(
            model_name='import',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='import',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='import',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='importfile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='importfile',
            name='file',
            field=models.FileField(storage=importer.models.UnuspiciousStorage(), max_length=1024, upload_to=importer.models.clean_upload_path),
        ),
        migrations.AlterField(
            model_name='importfile',
            name='messages',
            field=django_extensions.db.fields.json.JSONField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='importfile',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='importfile',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='importitem',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='importitem',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='importitem',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
        ),
    ]
