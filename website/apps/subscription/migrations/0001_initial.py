# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0012_auto_20150607_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='Name (internal)')),
                ('backend', models.CharField(default=b'mailchimp', max_length=36, choices=[(b'mailchimp', b'Mailchimp'), (b'madmimi', b'Madmimi (not implemented)')])),
                ('backend_id', models.CharField(max_length=64, null=True, blank=True)),
                ('backend_api_key', models.CharField(max_length=64, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Newsletter',
            },
        ),
        migrations.CreateModel(
            name='NewsletterTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title (translated)')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='subscription.Newsletter', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'subscription_newsletter_translation',
                'db_tablespace': '',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=256, null=True, blank=True)),
                ('name', models.CharField(max_length=256, null=True, blank=True)),
                ('backend_id', models.CharField(max_length=64, null=True, blank=True)),
                ('channel', models.CharField(max_length=256, null=True, blank=True)),
                ('language', models.CharField(max_length=5, null=True, blank=True)),
                ('opted_out', models.DateTimeField(null=True, blank=True)),
                ('confirmed', models.DateTimeField(null=True, blank=True)),
                ('newsletter', models.ForeignKey(blank=True, to='subscription.Newsletter', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Subscription',
            },
        ),
        migrations.CreateModel(
            name='SubscriptionButtonPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('button_text', models.CharField(default=b'Subscribe', max_length=64)),
                ('button_subline', models.TextField(max_length=64, null=True, blank=True)),
                ('popup_text', models.TextField(max_length=256, null=True, blank=True)),
                ('channel', models.CharField(default=b'general', max_length=32)),
                ('newsletter', models.ForeignKey(to='subscription.Newsletter', null=True)),
                ('redirect', cms.models.fields.PageField(blank=True, to='cms.Page', help_text='Redirect to page after successfull subscription', null=True, verbose_name='redirect on success')),
            ],
            bases=('cms.cmsplugin',),
        ),
        migrations.AlterUniqueTogether(
            name='newslettertranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
