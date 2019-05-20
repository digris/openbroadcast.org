# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields
import django_extensions.db.fields
import django.db.models.deletion
from django.conf import settings
import base.fields.extra
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('l10n', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('name', models.CharField(max_length=256, null=True, blank=True)),
                ('teaser', models.CharField(max_length=512, null=True, blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from='name', editable=False, blank=True)),
                ('type', models.CharField(default='stream', max_length=12, verbose_name='Type', choices=[('stream', 'Stream'), ('djmon', 'DJ-Monitor')])),
                ('stream_url', models.CharField(help_text='setting the stream-url overrides server settings', max_length=256, null=True, blank=True)),
                ('description', base.fields.extra.MarkdownTextField(null=True, blank=True)),
                ('rtmp_app', models.CharField(max_length=256, null=True, blank=True)),
                ('rtmp_path', models.CharField(max_length=256, null=True, blank=True)),
                ('has_scheduler', models.BooleanField(default=False)),
                ('mount', models.CharField(max_length=64, null=True, blank=True)),
                ('tunein_station_id', models.CharField(max_length=16, null=True, blank=True)),
                ('tunein_partner_id', models.CharField(max_length=16, null=True, blank=True)),
                ('tunein_partner_key', models.CharField(max_length=16, null=True, blank=True)),
                ('icecast2_server', models.CharField(max_length=256, null=True, blank=True)),
                ('icecast2_mountpoint', models.CharField(max_length=128, null=True, blank=True)),
                ('icecast2_admin_user', models.CharField(max_length=128, null=True, blank=True)),
                ('icecast2_admin_pass', models.CharField(max_length=128, null=True, blank=True)),
                ('on_air_id', models.PositiveIntegerField(null=True, blank=True)),
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
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('name', models.CharField(max_length=128, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('mood', models.TextField(null=True, blank=True)),
                ('sound', models.TextField(null=True, blank=True)),
                ('talk', models.TextField(null=True, blank=True)),
                ('enable_autopilot', models.BooleanField(default=True)),
                ('position', models.PositiveIntegerField(default=1, choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3')])),
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
                ('time_start', models.DateField(null=True)),
                ('time_end', models.DateField(null=True)),
                ('channel', models.ForeignKey(related_name='daypartsets', on_delete=django.db.models.deletion.SET_NULL, to='abcast.Channel', null=True)),
            ],
            options={
                'ordering': ('time_start',),
                'verbose_name': 'Daypart set',
                'verbose_name_plural': 'Daypart sets',
            },
        ),
        migrations.CreateModel(
            name='Emission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from='name', blank=True, overwrite=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Waiting'), (1, 'Done'), (2, 'Error')])),
                ('color', models.PositiveIntegerField(default=0, choices=[(0, 'Theme 1'), (1, 'Theme 2'), (2, 'Theme 3'), (3, 'Theme 4')])),
                ('type', models.CharField(default='playlist', max_length=12, verbose_name='Type', choices=[('studio', 'Studio'), ('playlist', 'Playlist'), ('couchcast', 'Couchcast')])),
                ('source', models.CharField(default='user', max_length=12, verbose_name='Source', choices=[('user', 'User'), ('autopilot', 'Autopilot')])),
                ('time_start', models.DateTimeField(null=True, blank=True)),
                ('time_end', models.DateTimeField(null=True, blank=True)),
                ('duration', models.PositiveIntegerField(verbose_name='Duration (in ms)', null=True, editable=False, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('locked', models.BooleanField(default=False)),
                ('channel', models.ForeignKey(related_name='scheduler_emissions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='abcast.Channel', null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='scheduler_emissions', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-time_start',),
                'verbose_name': 'Emission',
                'verbose_name_plural': 'Emissions',
                'permissions': (('schedule_emission', 'Schedule Emission'),),
            },
        ),
        migrations.CreateModel(
            name='OnAirItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
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
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('type', models.CharField(default='stream', max_length=12, verbose_name='Type', choices=[('stream', 'Stream'), ('djmon', 'DJ-Monitor')])),
                ('name', models.CharField(max_length=256, null=True, blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from='name', editable=False, blank=True)),
                ('teaser', models.CharField(max_length=512, null=True, blank=True)),
                ('main_image', models.ImageField(upload_to='abcast/station', null=True, verbose_name='Image', blank=True)),
                ('description', base.fields.extra.MarkdownTextField(null=True, blank=True)),
                ('website', models.URLField(max_length=256, null=True, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='phone', blank=True)),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='fax', blank=True)),
                ('address1', models.CharField(max_length=100, null=True, verbose_name='address', blank=True)),
                ('address2', models.CharField(max_length=100, null=True, verbose_name='address (secondary)', blank=True)),
                ('city', models.CharField(max_length=100, null=True, verbose_name='city', blank=True)),
                ('zip', models.CharField(max_length=10, null=True, verbose_name='zip', blank=True)),
                ('country', models.ForeignKey(blank=True, to='l10n.Country', null=True)),
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
            name='Weekday',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.PositiveIntegerField(default=0, choices=[(6, 'Sun'), (0, 'Mon'), (1, 'Tue'), (2, 'Wed'), (3, 'Thu'), (4, 'Fri'), (5, 'Sat')])),
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
        migrations.AlterUniqueTogether(
            name='onairitem',
            unique_together=set([('content_type', 'object_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='channel',
            unique_together=set([('on_air_type', 'on_air_id')]),
        ),
    ]
