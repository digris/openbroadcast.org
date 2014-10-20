# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Playout'
        db.create_table('bcmon_playout', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bcmon.Channel'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('bcmon', ['Playout'])

        # Adding model 'Channel'
        db.create_table('bcmon_channel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('slug', self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, populate_from='name', overwrite=False)),
            ('stream_url', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('title_format', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal('bcmon', ['Channel'])


    def backwards(self, orm):
        # Deleting model 'Playout'
        db.delete_table('bcmon_playout')

        # Deleting model 'Channel'
        db.delete_table('bcmon_channel')


    models = {
        'bcmon.channel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Channel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'stream_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'title_format': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'bcmon.playout': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Playout'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcmon.Channel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        }
    }

    complete_apps = ['bcmon']