# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django_extensions.db.fields
import lib.fields.extra
import abcast.models.jinglemodels
import django.db.models.deletion
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0002_auto_20151022_1756'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('filer', '0002_auto_20150606_2003'),
        ('l10n', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Broadcast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'name', blank=True, overwrite=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Waiting'), (1, 'Done'), (2, 'Error')])),
                ('type', models.CharField(default=b'jingle', max_length=12, verbose_name='Type', choices=[(b'studio', 'Studio'), (b'playlist', 'Playlist'), (b'couchcast', 'Couchcast')])),
                ('description', models.TextField(null=True, verbose_name=b'Extra Description', blank=True)),
                ('duration', models.PositiveIntegerField(null=True, verbose_name=b'Duration (in ms)', blank=True)),
                ('playlist', models.ForeignKey(related_name='scheduler_broadcasts', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='alibrary.Playlist', null=True)),
                ('user', models.ForeignKey(related_name='scheduler_broadcasts', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('created',),
                'verbose_name': 'Broadcast',
                'verbose_name_plural': 'Broadcasts',
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256, null=True, blank=True)),
                ('teaser', models.CharField(max_length=512, null=True, blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'name', editable=False, blank=True)),
                ('type', models.CharField(default=b'stream', max_length=12, verbose_name='Type', choices=[(b'stream', 'Stream'), (b'djmon', 'DJ-Monitor')])),
                ('stream_url', models.CharField(help_text='setting the stream-url overrides server settings', max_length=256, null=True, blank=True)),
                ('description', lib.fields.extra.MarkdownTextField(null=True, blank=True)),
                ('rtmp_app', models.CharField(max_length=256, null=True, blank=True)),
                ('rtmp_path', models.CharField(max_length=256, null=True, blank=True)),
                ('has_scheduler', models.BooleanField(default=False)),
                ('mount', models.CharField(max_length=64, null=True, blank=True)),
                ('on_air_id', models.PositiveIntegerField(null=True, blank=True)),
                ('description_html', models.TextField(null=True, editable=False, blank=True)),
                ('on_air_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Channel',
                'verbose_name_plural': 'Channels',
            },
        ),
        migrations.CreateModel(
            name='Daypart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('name', models.CharField(max_length=128, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('mood', models.TextField(null=True, blank=True)),
                ('sound', models.TextField(null=True, blank=True)),
                ('talk', models.TextField(null=True, blank=True)),
                ('position', models.PositiveIntegerField(default=1, choices=[(0, b'0'), (1, b'1'), (2, b'2'), (3, b'3')])),
            ],
            options={
                'ordering': ('position', 'time_start'),
                'verbose_name': 'Daypart',
                'verbose_name_plural': 'Dayparts',
            },
        ),
        migrations.CreateModel(
            name='DaypartSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('time_start', models.DateField(null=True)),
                ('time_end', models.DateField(null=True)),
                ('channel', models.ForeignKey(related_name='daypartsets', on_delete=django.db.models.deletion.SET_NULL, to='abcast.Channel', null=True)),
            ],
            options={
                'ordering': ('created',),
                'verbose_name': 'Daypart set',
                'verbose_name_plural': 'Daypart sets',
            },
        ),
        migrations.CreateModel(
            name='Emission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'name', blank=True, overwrite=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Waiting'), (1, 'Done'), (2, 'Error')])),
                ('color', models.PositiveIntegerField(default=0, choices=[(0, 'Theme 1'), (1, 'Theme 2'), (2, 'Theme 3'), (3, 'Theme 4')])),
                ('type', models.CharField(default=b'playlist', max_length=12, verbose_name='Type', choices=[(b'studio', 'Studio'), (b'playlist', 'Playlist'), (b'couchcast', 'Couchcast')])),
                ('source', models.CharField(default=b'user', max_length=12, verbose_name='Source', choices=[(b'user', 'User'), (b'autopilot', 'Autopilot')])),
                ('time_start', models.DateTimeField(null=True, blank=True)),
                ('time_end', models.DateTimeField(null=True, blank=True)),
                ('duration', models.PositiveIntegerField(verbose_name=b'Duration (in ms)', null=True, editable=False, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('locked', models.BooleanField(default=False)),
                ('channel', models.ForeignKey(related_name='scheduler_emissions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='abcast.Channel', null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='scheduler_emissions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('created',),
                'verbose_name': 'Emission',
                'verbose_name_plural': 'Emissions',
                'permissions': (('schedule_emission', 'Schedule Emission'),),
            },
        ),
        migrations.CreateModel(
            name='Jingle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'name', blank=True, overwrite=True)),
                ('processed', models.PositiveIntegerField(default=0, choices=[(0, 'Waiting'), (1, 'Done'), (2, 'Error')])),
                ('conversion_status', models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Completed'), (2, 'Error')])),
                ('lock', models.PositiveIntegerField(default=0, editable=False)),
                ('type', models.CharField(default=b'jingle', max_length=12, verbose_name='Type', choices=[(b'jingle', 'Jingle'), (b'placeholder', 'Placeholder')])),
                ('description', models.TextField(null=True, verbose_name=b'Extra Description', blank=True)),
                ('duration', models.PositiveIntegerField(null=True, verbose_name=b'Duration (in ms)', blank=True)),
                ('master', models.FileField(max_length=1024, null=True, upload_to=abcast.models.jinglemodels.masterpath_by_uuid, blank=True)),
                ('master_sha1', models.CharField(db_index=True, max_length=64, null=True, blank=True)),
                ('folder', models.CharField(max_length=1024, null=True, editable=False, blank=True)),
                ('artist', models.ForeignKey(related_name='jingle_artist', blank=True, to='alibrary.Artist', null=True)),
            ],
            options={
                'ordering': ('created',),
                'verbose_name': 'Jingle',
                'verbose_name_plural': 'Jingles',
            },
        ),
        migrations.CreateModel(
            name='JingleSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'name', blank=True, overwrite=True)),
                ('description', models.TextField(null=True, verbose_name=b'Extra Description', blank=True)),
                ('main_image', filer.fields.image.FilerImageField(related_name='jingleset_main_image', blank=True, to='filer.Image', null=True)),
            ],
            options={
                'ordering': ('created',),
                'verbose_name': 'Jingle-Set',
                'verbose_name_plural': 'Jingle-Sets',
            },
        ),
        migrations.CreateModel(
            name='OnAirItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'On Air',
                'verbose_name_plural': 'On Air',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256, null=True, blank=True)),
                ('teaser', models.CharField(max_length=512, null=True, blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'name', editable=False, blank=True)),
                ('type', models.CharField(default=b'stream', max_length=12, verbose_name='Type', choices=[(b'stream', 'Stream'), (b'djmon', 'DJ-Monitor')])),
                ('description', lib.fields.extra.MarkdownTextField(null=True, blank=True)),
                ('website', models.URLField(max_length=256, null=True, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='phone', blank=True)),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='fax', blank=True)),
                ('address1', models.CharField(max_length=100, null=True, verbose_name='address', blank=True)),
                ('address2', models.CharField(max_length=100, null=True, verbose_name='address (secondary)', blank=True)),
                ('city', models.CharField(max_length=100, null=True, verbose_name='city', blank=True)),
                ('zip', models.CharField(max_length=10, null=True, verbose_name='zip', blank=True)),
                ('description_html', models.TextField(null=True, editable=False, blank=True)),
                ('country', models.ForeignKey(blank=True, to='l10n.Country', null=True)),
                ('main_image', filer.fields.image.FilerImageField(related_name='station_main_image', blank=True, to='filer.Image', null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Station',
                'verbose_name_plural': 'Stations',
            },
        ),
        migrations.CreateModel(
            name='StationMembers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roles', models.ManyToManyField(related_name='memgership_roles', to='abcast.Role', blank=True)),
                ('station', models.ForeignKey(to='abcast.Station')),
                ('user', models.ForeignKey(related_name='station_membership', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='StreamFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('type', models.CharField(default=b'mp3', max_length=12, choices=[(b'mp3', 'MP3'), (b'ogg', 'ogg/vorbis'), (b'aac', 'AAC')])),
                ('bitrate', models.PositiveIntegerField(default=256, choices=[(64, '64 kbps'), (96, '96 kbps'), (128, '128 kbps'), (160, '160 kbps'), (192, '192 kbps'), (256, '256 kbps'), (320, '320 kbps')])),
            ],
            options={
                'ordering': ('type',),
                'verbose_name': 'Streaming format',
                'verbose_name_plural': 'Streaming formats',
            },
        ),
        migrations.CreateModel(
            name='StreamServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256, null=True)),
                ('host', models.URLField(max_length=256, null=True)),
                ('source_user', models.CharField(default=b'source', max_length=64, null=True, blank=True)),
                ('source_pass', models.CharField(max_length=64, null=True, blank=True)),
                ('admin_user', models.CharField(default=b'admin', max_length=64, null=True, blank=True)),
                ('admin_pass', models.CharField(max_length=64, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('mountpoint', models.CharField(help_text='e.g. main-hifi.mp3', max_length=64, null=True)),
                ('meta_prefix', models.CharField(help_text='e.g. My Station!', max_length=64, null=True, blank=True)),
                ('type', models.CharField(default=b'icecast2', max_length=12, verbose_name='Type', choices=[(b'icecast2', 'Icecast 2'), (b'rtmp', 'RTMP / Wowza')])),
                ('formats', models.ManyToManyField(to='abcast.StreamFormat', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Streaming server',
                'verbose_name_plural': 'Streaming servers',
            },
        ),
        migrations.CreateModel(
            name='Weekday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.PositiveIntegerField(default=1, choices=[(1, 'Sun'), (2, 'Mon'), (3, 'Tue'), (4, 'Wed'), (5, 'Thu'), (6, 'Fri'), (7, 'Sat')])),
            ],
            options={
                'ordering': ('day',),
                'verbose_name': 'Weekay',
                'verbose_name_plural': 'Weekays',
            },
        ),
        migrations.AddField(
            model_name='station',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='abcast.StationMembers', blank=True),
        ),
        migrations.AddField(
            model_name='jingleset',
            name='station',
            field=models.ForeignKey(related_name='jingleset_station', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='abcast.Station', null=True),
        ),
        migrations.AddField(
            model_name='jingle',
            name='set',
            field=models.ForeignKey(related_name='jingle_set', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='abcast.JingleSet', null=True),
        ),
        migrations.AddField(
            model_name='jingle',
            name='user',
            field=models.ForeignKey(related_name='jingle_user', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='daypart',
            name='daypartset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='abcast.DaypartSet', null=True),
        ),
        migrations.AddField(
            model_name='daypart',
            name='weekdays',
            field=models.ManyToManyField(to='abcast.Weekday', blank=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='abcast.Station', null=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='stream_server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='abcast.StreamServer', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='onairitem',
            unique_together=set([('content_type', 'object_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='channel',
            unique_together=set([('on_air_type', 'on_air_id')]),
        ),
    ]
