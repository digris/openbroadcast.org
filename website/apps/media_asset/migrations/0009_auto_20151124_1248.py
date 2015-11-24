# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_asset', '0008_waveform_accessed'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='format',
            unique_together=set([('media', 'encoding', 'quality')]),
        ),
        migrations.AlterUniqueTogether(
            name='waveform',
            unique_together=set([('media', 'type')]),
        ),
    ]
