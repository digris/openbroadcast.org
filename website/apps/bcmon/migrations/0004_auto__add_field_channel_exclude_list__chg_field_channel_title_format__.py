# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Channel.exclude_list'
        db.add_column('bcmon_channel', 'exclude_list',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Channel.title_format'
        db.alter_column('bcmon_channel', 'title_format', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'Channel.stream_url'
        db.alter_column('bcmon_channel', 'stream_url', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'Channel.name'
        db.alter_column('bcmon_channel', 'name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

    def backwards(self, orm):
        # Deleting field 'Channel.exclude_list'
        db.delete_column('bcmon_channel', 'exclude_list')


        # Changing field 'Channel.title_format'
        db.alter_column('bcmon_channel', 'title_format', self.gf('django.db.models.fields.CharField')(default='', max_length=256))

        # Changing field 'Channel.stream_url'
        db.alter_column('bcmon_channel', 'stream_url', self.gf('django.db.models.fields.CharField')(default='', max_length=256))

        # Changing field 'Channel.name'
        db.alter_column('bcmon_channel', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=256))

    models = {
        'bcmon.channel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Channel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'exclude_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'stream_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'title_format': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'bcmon.playout': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Playout'},
            'analyzer_data': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcmon.Channel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sample': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        }
    }

    complete_apps = ['bcmon']