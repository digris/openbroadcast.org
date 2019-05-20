# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import exporter.models
import django.db.models.deletion
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Export',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Progress'), (4, 'Downloaded'), (99, 'Error'), (11, 'Other')])),
                ('status_msg', models.CharField(max_length=512, null=True, blank=True)),
                ('filesize', models.IntegerField(default=0, null=True, blank=True)),
                ('filename', models.CharField(max_length=256, null=True, blank=True)),
                ('file', models.FileField(null=True, upload_to=exporter.models.create_download_path, blank=True)),
                ('fileformat', models.CharField(default=b'mp3', max_length=4, choices=[(b'mp3', 'MP3'), (b'flac', 'Flac')])),
                ('token', models.CharField(max_length=256, null=True, blank=True)),
                ('downloaded', models.DateTimeField(null=True, blank=True)),
                ('type', models.CharField(default=b'web', max_length=10, choices=[(b'web', 'Web Interface'), (b'api', 'API'), (b'fs', 'Filesystem')])),
                ('notes', models.TextField(help_text='Optionally, just add some notes to this export if desired.', null=True, blank=True)),
                ('user', models.ForeignKey(related_name='exports', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('created',),
                'verbose_name': 'Export',
                'verbose_name_plural': 'Exports',
            },
        ),
        migrations.CreateModel(
            name='ExportItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Progress'), (4, 'Downloaded'), (99, 'Error'), (11, 'Other')])),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('export_session', models.ForeignKey(related_name='export_items', verbose_name='Export', to='exporter.Export', null=True)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Export Item',
                'verbose_name_plural': 'Export Items',
            },
        ),
    ]
