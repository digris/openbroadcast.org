# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Playout.meta_title'
        db.delete_column('bcmon_playout', 'meta_title')

        # Adding field 'Playout.meta_artist'
        db.add_column('bcmon_playout', 'meta_artist',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Playout.meta_title'
        db.add_column('bcmon_playout', 'meta_title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=512, blank=True),
                      keep_default=False)

        # Deleting field 'Playout.meta_artist'
        db.delete_column('bcmon_playout', 'meta_artist')


    models = {
        'bcmon.channel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Channel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enable_monitoring': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'exclude_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'stream_url': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'title_format': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'title_only_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'bcmon.playout': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Playout'},
            'analyzer_data': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bcmon.Channel']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'enmfp': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_artist': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'meta_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'sample': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        }
    }

    complete_apps = ['bcmon']