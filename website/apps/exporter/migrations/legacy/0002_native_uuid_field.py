# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def concat_uuids(apps, schema_editor):

    items = [
        'Export',
        'ExportItem',
    ]

    for item in items:
        qs = apps.get_model("exporter", item)
        print('concat uuids on {}'.format(item))
        for obj in qs.objects.using(schema_editor.connection.alias).all():
            qs.objects.filter(pk=obj.pk).update(uuid=obj.uuid.replace('-', ''))


class Migration(migrations.Migration):

    dependencies = [
        ('exporter', '0001_initial'),
    ]

    operations = [

        migrations.RunPython(concat_uuids),

        migrations.AlterField(
            model_name='export',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='export',
            name='type',
            field=models.CharField(default=b'web', max_length=10, choices=[(b'web', 'Web Interface'), (b'api', 'API'), (b'fs', 'Filesystem')]),
        ),
        migrations.AlterField(
            model_name='export',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='export',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='exportitem',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='exportitem',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='exportitem',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, db_index=True),
        ),
    ]
