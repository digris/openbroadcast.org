# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields
import django.db.models.deletion
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Massimport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Queued'), (99, 'Error')])),
                ('directory', models.CharField(max_length=1024)),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('collection_name', models.CharField(max_length=250, null=True, blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Import',
                'verbose_name_plural': 'Imports',
                'permissions': (('massimport_manage', 'Manage Massimporter Sessions'),),
            },
        ),
        migrations.CreateModel(
            name='MassimportFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('status', models.PositiveIntegerField(default=0, db_index=True, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Working'), (4, 'Warning'), (5, 'Duplicate'), (6, 'Queued'), (7, 'Importing'), (99, 'Error'), (11, 'Other')])),
                ('path', models.CharField(max_length=1024)),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('import_file', models.ForeignKey(to='importer.ImportFile', null=True)),
                ('massimport', models.ForeignKey(related_name='files', to='massimporter.Massimport')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
        ),
    ]
