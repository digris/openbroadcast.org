# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import importer.models
import django_extensions.db.fields
import django_extensions.db.fields.json
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0002_auto_20151022_1756'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('uuid_key', models.CharField(max_length=60, null=True, blank=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Progress'), (99, 'Error'), (11, 'Other')])),
                ('type', models.CharField(default=b'web', max_length=b'10', choices=[(b'web', 'Web Interface'), (b'api', 'API'), (b'fs', 'Filesystem')])),
                ('notes', models.TextField(help_text='Optionally, just add some notes to this import if desired.', null=True, blank=True)),
                ('user', models.ForeignKey(related_name='import_user', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Import',
                'verbose_name_plural': 'Imports',
            },
        ),
        migrations.CreateModel(
            name='ImportFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('filename', models.CharField(max_length=256, null=True, blank=True)),
                ('file', models.FileField(max_length=256, upload_to=importer.models.clean_upload_path)),
                ('mimetype', models.CharField(max_length=100, null=True, blank=True)),
                ('messages', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('settings', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('results_tag', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('results_tag_status', models.PositiveIntegerField(default=0, verbose_name='Result Tags (ID3 & co)', choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Progress'), (99, 'Error'), (11, 'Other')])),
                ('results_acoustid', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('results_acoustid_status', models.PositiveIntegerField(default=0, verbose_name='Result Musicbrainz', choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Progress'), (99, 'Error'), (11, 'Other')])),
                ('results_musicbrainz', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('results_discogs_status', models.PositiveIntegerField(default=0, verbose_name='Result Musicbrainz', choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Progress'), (99, 'Error'), (11, 'Other')])),
                ('results_discogs', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('import_tag', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('imported_api_url', models.CharField(max_length=512, null=True, blank=True)),
                ('error', models.CharField(max_length=512, null=True, blank=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Working'), (4, 'Warning'), (5, 'Duplicate'), (6, 'Queued'), (7, 'Importing'), (99, 'Error'), (11, 'Other')])),
                ('import_session', models.ForeignKey(related_name='files', verbose_name='Import', to='importer.Import', null=True)),
                ('media', models.ForeignKey(related_name='importfile_media', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='alibrary.Media', null=True)),
            ],
            options={
                'ordering': ('created',),
                'verbose_name': 'Import File',
                'verbose_name_plural': 'Import Files',
            },
        ),
        migrations.CreateModel(
            name='ImportItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('import_session', models.ForeignKey(related_name='importitem_set', verbose_name='Import', to='importer.Import', null=True)),
            ],
            options={
                'verbose_name': 'Import Item',
                'verbose_name_plural': 'Import Items',
            },
        ),
    ]
