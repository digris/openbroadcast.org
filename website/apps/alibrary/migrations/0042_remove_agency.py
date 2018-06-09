# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0041_auto_20180608_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agency',
            name='artists',
        ),
        migrations.RemoveField(
            model_name='agency',
            name='country',
        ),
        migrations.RemoveField(
            model_name='agency',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='agency',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='agency',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='agency',
            name='publisher',
        ),
        migrations.RemoveField(
            model_name='agencyartist',
            name='agency',
        ),
        migrations.RemoveField(
            model_name='agencyartist',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='agencyartist',
            name='countries',
        ),
        migrations.RemoveField(
            model_name='agencyartist',
            name='scopes',
        ),
        migrations.DeleteModel(
            name='Agency',
        ),
        migrations.DeleteModel(
            name='AgencyArtist',
        ),
        migrations.DeleteModel(
            name='AgencyScope',
        ),
    ]
