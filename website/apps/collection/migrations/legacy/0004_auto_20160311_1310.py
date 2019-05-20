# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collection', '0003_auto_20160224_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollectionMaintainer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='collection',
            name='user',
        ),
        migrations.AddField(
            model_name='collectionmaintainer',
            name='collection',
            field=models.ForeignKey(to='collection.Collection'),
        ),
        migrations.AddField(
            model_name='collectionmaintainer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collection',
            name='maintainers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='collection.CollectionMaintainer', blank=True),
        ),
    ]
