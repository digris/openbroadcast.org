# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import bcmon.models
import django.db.models.deletion
import django_extensions.db.fields
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0002_auto_20151022_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256, null=True, blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'name', editable=False, blank=True)),
                ('type', models.CharField(default=b'stream', max_length=12, verbose_name='Type', choices=[(b'stream', 'Stream'), (b'djmon', 'DJ-Monitor')])),
                ('stream_url', models.CharField(max_length=256, null=True, blank=True)),
                ('title_format', models.CharField(help_text=b'Regex to match title against. eg "(?P<artist>[\\w\\s\\d +"*\xc3\xa7%&/(),.-;:_]+?)-(?P<track>[\\w\\s\\d +"*\xc3\xa7%&/(),.-;:_]+?)$" to recognize formats like "The Prodigy  (feat. Whomever) - Remix 3000" - (incl. unicode)', max_length=256, null=True, blank=True)),
                ('exclude_list', models.TextField(help_text='Comma separated, keywords that should completely be ignored.', null=True, blank=True)),
                ('title_only_list', models.TextField(help_text="Comma separated, only track titles but don' analyze.", null=True, blank=True)),
                ('enable_monitoring', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Channel',
                'verbose_name_plural': 'Channels',
            },
        ),
        migrations.CreateModel(
            name='Playout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=512, blank=True)),
                ('meta_name', models.CharField(max_length=512, blank=True)),
                ('meta_artist', models.CharField(max_length=512, blank=True)),
                ('dummy_result', models.CharField(max_length=512, blank=True)),
                ('time_start', models.DateTimeField(null=True, blank=True)),
                ('time_end', models.DateTimeField(null=True, blank=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Waiting'), (1, 'Done'), (2, 'Ready'), (3, 'Error'), (4, 'Echoprint directly (no sample)')])),
                ('score', models.PositiveIntegerField(default=0)),
                ('sample', models.FileField(null=True, upload_to=bcmon.models.filename_by_uuid, blank=True)),
                ('analyzer_data', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('enmfp', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('echoprint_data', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('echoprintfp', django_extensions.db.fields.json.JSONField(null=True, blank=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='bcmon.Channel', null=True)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='alibrary.Media', null=True)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Playout',
                'verbose_name_plural': 'Playouts',
            },
        ),
    ]
