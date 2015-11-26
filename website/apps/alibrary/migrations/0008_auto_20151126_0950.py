# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alibrary', '0007_auto_20151123_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='last_editor',
            field=models.ForeignKey(related_name='artists_last_editor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='label',
            name='last_editor',
            field=models.ForeignKey(related_name='labels_last_editor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='media',
            name='last_editor',
            field=models.ForeignKey(related_name='media_last_editor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='release',
            name='last_editor',
            field=models.ForeignKey(related_name='releases_last_editor', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='license',
            name='uuid',
            field=models.CharField(default=b'<function uuid4 at 0x100f25ed8>', max_length=36, editable=False),
        ),
        migrations.AlterField(
            model_name='namevariation',
            name='artist',
            field=models.ForeignKey(related_name='namevariations', blank=True, to='alibrary.Artist', null=True),
        ),
    ]
