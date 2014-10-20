# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Match.title'
        db.add_column('spf_match', 'title',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Match.title'
        db.delete_column('spf_match', 'title')


    models = {
        'spf.match': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Match'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'artist_credits': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'artist_credits_secondary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isrc_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'iswc_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mb_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'release': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'release_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spf.Request']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'results_mb': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'work_list': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'spf.request': {
            'Meta': {'ordering': "('swp_id',)", 'object_name': 'Request'},
            'catalognumber': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'composer': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isrc': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'main_artist': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'num_results': ('django.db.models.fields.IntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'obp_legacy_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'publication_datex': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recording_country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'recording_date': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'recording_datex': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'results_mb': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'null': 'True', 'blank': 'True'}),
            'rome_protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'swp_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['spf']