# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def concat_uuids(apps, schema_editor):

    items = [
        'Agency',
        'Distributor',
        'Media',
        'Playlist',
        'Playlistitem',
        'Playlistitemplaylist',
        'Playlistmedia',
        'Release',
        'Series',
    ]

    for item in items:
        qs = apps.get_model("alibrary", item)
        for object in qs.objects.using(schema_editor.connection.alias).all():
            qs.objects.filter(pk=object.pk).update(uuid=object.uuid.replace('-', ''))



def forwards(apps, schema_editor):
    if not schema_editor.connection.vendor == 'postgresql':
        print('db backend not postgres - skipping table update')
        return
    migrations.RunSQL("""
alter table alibrary_agency alter column uuid type uuid using uuid::uuid;
alter table alibrary_distributor alter column uuid type uuid using uuid::uuid;
alter table alibrary_media alter column uuid type uuid using uuid::uuid;
alter table alibrary_playlist alter column uuid type uuid using uuid::uuid;
alter table alibrary_playlistitem alter column uuid type uuid using uuid::uuid;
alter table alibrary_playlistitemplaylist alter column uuid type uuid using uuid::uuid;
alter table alibrary_playlistmedia alter column uuid type uuid using uuid::uuid;
alter table alibrary_release alter column uuid type uuid using uuid::uuid;
alter table alibrary_series alter column uuid type uuid using uuid::uuid;
""")



class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0020_auto_20160220_1727'),
    ]

    operations = [
        migrations.RunPython(concat_uuids),

        migrations.RunPython(forwards, None, [

            migrations.AlterField(
                model_name='agency',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
            migrations.AlterField(
                model_name='distributor',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
            migrations.AlterField(
                model_name='media',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
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
                model_name='playlistmedia',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
            migrations.AlterField(
                model_name='release',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
            migrations.AlterField(
                model_name='series',
                name='uuid',
                field=models.UUIDField(default=uuid.uuid4, editable=False),
            ),
        ]),

    ]
