# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0047_fix_base_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='parent_temporary_id',
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
            name='creator',
            field=models.ForeignKey(related_name='created_media', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
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
            name='type',
            field=models.CharField(default='basket', max_length=12, null=True, choices=[('basket', 'Private Playlist'), ('playlist', 'Public Playlist'), ('broadcast', 'Broadcast'), ('other', 'Other')]),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(related_name='playlists', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
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
            name='item',
            field=models.ForeignKey(related_name='playlist_items', to='alibrary.PlaylistItem'),
        ),
        migrations.AlterField(
            model_name='playlistitemplaylist',
            name='playlist',
            field=models.ForeignKey(related_name='playlist_items', to='alibrary.Playlist'),
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
            name='object_id',
            field=models.PositiveIntegerField(db_index=True),
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
    ]
