# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields
import base.fields.extra
import tagging.fields
import profiles.models
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('l10n', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('legacy_id', models.IntegerField(null=True, editable=False, blank=True)),
                ('legacy_legacy_id', models.IntegerField(null=True, editable=False, blank=True)),
                ('migrated', models.DateField(null=True, editable=False, blank=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(editable=False, populate_from=b'name', blank=True, overwrite=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('description', base.fields.extra.MarkdownTextField(null=True, blank=True)),
                ('image', models.ImageField(upload_to=profiles.models.filename_by_uuid, null=True, verbose_name='Profile Image', blank=True)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='mobile', blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='phone', blank=True)),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='fax', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('address1', models.CharField(max_length=100, null=True, verbose_name='address', blank=True)),
                ('address2', models.CharField(max_length=100, null=True, verbose_name='address (secondary)', blank=True)),
                ('city', models.CharField(max_length=100, null=True, verbose_name='city', blank=True)),
                ('zip', models.CharField(max_length=10, null=True, verbose_name='zip', blank=True)),
                ('d_tags', tagging.fields.TagField(max_length=255, null=True, verbose_name=b'Tags', blank=True)),
                ('description_html', models.TextField(null=True, editable=False, blank=True)),
                ('country', models.ForeignKey(blank=True, to='l10n.Country', null=True)),
            ],
            options={
                'verbose_name': 'Community',
                'verbose_name_plural': 'Communities',
            },
        ),
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Expertise',
                'verbose_name_plural': 'Expertise',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, verbose_name='title', blank=True)),
                ('url', models.URLField(verbose_name='url')),
            ],
            options={
                'db_table': 'user_links',
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
            },
        ),
        migrations.CreateModel(
            name='MobileProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=25, verbose_name='title')),
                ('domain', models.CharField(unique=True, max_length=50, verbose_name='domain')),
            ],
            options={
                'db_table': 'user_mobile_providers',
                'verbose_name': 'mobile provider',
                'verbose_name_plural': 'mobile providers',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('legacy_id', models.IntegerField(null=True, editable=False, blank=True)),
                ('legacy_legacy_id', models.IntegerField(null=True, editable=False, blank=True)),
                ('migrated', models.DateField(null=True, editable=False, blank=True)),
                ('uuid', django_extensions.db.fields.UUIDField(editable=False, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('gender', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='gender', choices=[(0, 'Male'), (1, 'Female'), (2, 'Other')])),
                ('birth_date', models.DateField(help_text='Format: YYYY-MM-DD', null=True, verbose_name='Date of birth', blank=True)),
                ('pseudonym', models.CharField(max_length=250, null=True, blank=True)),
                ('description', models.CharField(max_length=250, null=True, verbose_name='Disambiguation', blank=True)),
                ('biography', base.fields.extra.MarkdownTextField(null=True, blank=True)),
                ('image', models.ImageField(upload_to=profiles.models.filename_by_uuid, null=True, verbose_name='Profile Image', blank=True)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='mobile', blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='phone', blank=True)),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, verbose_name='fax', blank=True)),
                ('address1', models.CharField(max_length=100, null=True, verbose_name='address', blank=True)),
                ('address2', models.CharField(max_length=100, null=True, verbose_name='address (secondary)', blank=True)),
                ('city', models.CharField(max_length=100, null=True, verbose_name='city', blank=True)),
                ('zip', models.CharField(max_length=10, null=True, verbose_name='zip', blank=True)),
                ('iban', models.CharField(max_length=120, null=True, verbose_name='IBAN', blank=True)),
                ('paypal', models.EmailField(max_length=200, null=True, verbose_name='Paypal', blank=True)),
                ('d_tags', tagging.fields.TagField(max_length=1024, null=True, verbose_name=b'Tags', blank=True)),
                ('enable_alpha_features', models.BooleanField(default=False)),
                ('biography_html', models.TextField(null=True, editable=False, blank=True)),
                ('country', models.ForeignKey(blank=True, to='l10n.Country', null=True)),
                ('expertise', models.ManyToManyField(to='profiles.Expertise', verbose_name='Fields of expertise', blank=True)),
                ('mentor', models.ForeignKey(related_name='godchildren', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-user__last_login',),
                'db_table': 'user_profiles',
                'verbose_name': 'user profile',
                'verbose_name_plural': 'user profiles',
                'permissions': (('mentor_profiles', 'Mentoring profiles'), ('view_profiles_private', 'View private profile-data.')),
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=100, verbose_name='Userame / ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(to='profiles.Profile')),
            ],
            options={
                'db_table': 'user_services',
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title', blank=True)),
                ('url', models.URLField(help_text=b"URL with a single '{user}' placeholder to turn a username into a service URL.", verbose_name='url', blank=True)),
            ],
            options={
                'db_table': 'user_service_types',
                'verbose_name': 'service type',
                'verbose_name_plural': 'service types',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='service',
            field=models.ForeignKey(to='profiles.ServiceType'),
        ),
        migrations.AddField(
            model_name='link',
            name='profile',
            field=models.ForeignKey(to='profiles.Profile'),
        ),
        migrations.AddField(
            model_name='community',
            name='expertise',
            field=models.ManyToManyField(to='profiles.Expertise', verbose_name='Fields of expertise', blank=True),
        ),
        migrations.AddField(
            model_name='community',
            name='group',
            field=models.OneToOneField(null=True, blank=True, to='auth.Group'),
        ),
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
