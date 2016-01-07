# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=254)),
                ('ip', models.IPAddressField()),
            ],
            options={
                'ordering': ['hostname'],
                'verbose_name': 'Host',
            },
        ),
    ]
