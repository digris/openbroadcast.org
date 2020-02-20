# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_convert_services_to_relations'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='d_tags',
            field=tagging.fields.TagField(max_length=1024, null=True, verbose_name='Tags', blank=True),
        ),
    ]
