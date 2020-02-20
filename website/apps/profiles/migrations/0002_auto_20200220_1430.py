# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='community',
            name='d_tags',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='d_tags',
        ),
        migrations.AddField(
            model_name='community',
            name='tags',
            field=tagging.fields.TagField(max_length=255, null=True, verbose_name='Tags', blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='skype',
            field=models.CharField(max_length=100, null=True, verbose_name='Skype', blank=True),
        ),
    ]
