# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, null=True)),
                ('slug', models.SlugField()),
                ('public', models.BooleanField(default=True)),
                ('path', models.CharField(max_length=1024)),
            ],
        ),
    ]
