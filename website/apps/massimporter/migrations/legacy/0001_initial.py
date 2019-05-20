# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Massimport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Progress'), (99, 'Error'), (11, 'Other')])),
                ('directory', models.CharField(max_length=512)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Import',
                'verbose_name_plural': 'Imports',
            },
        ),
        migrations.CreateModel(
            name='MassimportFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('status', models.PositiveIntegerField(default=0, choices=[(0, 'Init'), (1, 'Done'), (2, 'Ready'), (3, 'Progress'), (99, 'Error'), (11, 'Other')])),
                ('path', models.CharField(max_length=512)),
                ('massimport', models.ForeignKey(related_name='files', to='massimporter.Massimport')),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
        ),
    ]
