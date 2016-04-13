# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_auto_20151208_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('summary', models.TextField(null=True, blank=True)),
                ('step_numbers', models.BooleanField(default=True)),
                ('include_toc', models.BooleanField(default=False, verbose_name=b'Include Table of Content')),
            ],
            options={
                'verbose_name': 'Step Guide',
                'verbose_name_plural': 'Step Guides',
            },
        ),
        migrations.CreateModel(
            name='GuidePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('guide', models.ForeignKey(to='stepguide.Guide')),
            ],
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('hint', models.TextField(null=True, blank=True)),
                ('hint_type', models.CharField(default=b'info', max_length=10, choices=[(b'info', b'Info (green)'), (b'warning', b'Warning (yellow)'), (b'critical', b'Critical (red)')])),
                ('image', models.ImageField(null=True, upload_to=b'stepguide', blank=True)),
                ('image_caption', models.CharField(max_length=255, null=True, blank=True)),
                ('vimeo_video_id', models.CharField(help_text=b'Show vimeo video. If id is set, the video will be displayed instead of an image.', max_length=255, null=True, blank=True)),
                ('position', models.PositiveSmallIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('guide', models.ForeignKey(blank=True, to='stepguide.Guide', null=True)),
            ],
            options={
                'ordering': ['-position'],
                'verbose_name': 'Step',
                'verbose_name_plural': 'Steps',
            },
        ),
    ]
