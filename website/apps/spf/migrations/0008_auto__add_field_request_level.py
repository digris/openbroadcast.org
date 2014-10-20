# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Request.level'
        db.add_column('spf_request', 'level',
                      self.gf('django.db.models.fields.IntegerField')(max_length=12, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Request.level'
        db.delete_column('spf_request', 'level')


    models = {
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
            'publication_date': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'publication_datex': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recording_country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'recording_date': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'recording_datex': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'rome_protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'swp_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['spf']