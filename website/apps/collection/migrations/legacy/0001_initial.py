# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=255)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('name', models.CharField(max_length=250, db_index=True)),
                ('slug', models.SlugField(editable=False, blank=True)),
                ('visibility', models.PositiveIntegerField(default=0, choices=[(0, 'private'), (1, 'public')])),
                ('description', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Collection',
                'verbose_name_plural': 'Collections',
            },
        ),
    ]
