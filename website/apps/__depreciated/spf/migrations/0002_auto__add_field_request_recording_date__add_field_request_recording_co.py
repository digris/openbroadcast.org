# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Request.recording_date'
        db.add_column('spf_request', 'recording_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Request.recording_country'
        db.add_column('spf_request', 'recording_country',
                      self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Request.rome_protected'
        db.add_column('spf_request', 'rome_protected',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Request.main_artist'
        db.add_column('spf_request', 'main_artist',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Request.publication_date'
        db.add_column('spf_request', 'publication_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Request.composer'
        db.add_column('spf_request', 'composer',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Request.label'
        db.add_column('spf_request', 'label',
                      self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Request.catalognumber'
        db.add_column('spf_request', 'catalognumber',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Request.isrc'
        db.add_column('spf_request', 'isrc',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Request.recording_date'
        db.delete_column('spf_request', 'recording_date')

        # Deleting field 'Request.recording_country'
        db.delete_column('spf_request', 'recording_country')

        # Deleting field 'Request.rome_protected'
        db.delete_column('spf_request', 'rome_protected')

        # Deleting field 'Request.main_artist'
        db.delete_column('spf_request', 'main_artist')

        # Deleting field 'Request.publication_date'
        db.delete_column('spf_request', 'publication_date')

        # Deleting field 'Request.composer'
        db.delete_column('spf_request', 'composer')

        # Deleting field 'Request.label'
        db.delete_column('spf_request', 'label')

        # Deleting field 'Request.catalognumber'
        db.delete_column('spf_request', 'catalognumber')

        # Deleting field 'Request.isrc'
        db.delete_column('spf_request', 'isrc')


    models = {
        'spf.request': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Request'},
            'catalognumber': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'composer': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isrc': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'main_artist': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recording_country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'recording_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'rome_protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'swp_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['spf']