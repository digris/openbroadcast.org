# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alibrary', '0035_auto_20170821_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreflightCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=1, db_index=True, verbose_name='Status', choices=[(0, 'Initialized'), (1, 'Pending'), (2, 'Processing'), (3, 'Done'), (99, 'Error')])),
                ('media', models.OneToOneField(related_name='preflight_check', null=True, to='alibrary.Media')),
            ],
        ),
    ]
