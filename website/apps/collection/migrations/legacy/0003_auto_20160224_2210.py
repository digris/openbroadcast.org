# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('collection', '0002_auto_20160224_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Collection Item',
                'verbose_name_plural': 'Collection Items',
            },
        ),
        migrations.CreateModel(
            name='CollectionMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('collection', models.ForeignKey(to='collection.Collection')),
                ('item', models.ForeignKey(to='collection.CollectionItem')),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='items',
            field=models.ManyToManyField(to='collection.CollectionItem', through='collection.CollectionMember', blank=True),
        ),
    ]
