# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'KeyValue', fields ['language', 'digest']
        try:
            db.delete_unique('datatrans_keyvalue', ['language', 'digest'])
        except ValueError:
            print "  WARNING: current index didn't exist"

        # Changing field 'KeyValue.field'
        db.alter_column('datatrans_keyvalue', 'field', self.gf('django.db.models.fields.CharField')(max_length=255))
        # Adding unique constraint on 'KeyValue', fields ['field', 'digest', 'content_type', 'language', 'object_id']
        db.create_unique('datatrans_keyvalue', ['field', 'digest', 'content_type_id', 'language', 'object_id'])

    def backwards(self, orm):
        # Removing unique constraint on 'KeyValue', fields ['field', 'digest', 'content_type', 'language', 'object_id']
        db.delete_unique('datatrans_keyvalue', ['field', 'digest', 'content_type_id', 'language', 'object_id'])


        # Changing field 'KeyValue.field'
        db.alter_column('datatrans_keyvalue', 'field', self.gf('django.db.models.fields.TextField')())
        # Adding unique constraint on 'KeyValue', fields ['language', 'digest']
        db.create_unique('datatrans_keyvalue', ['language', 'digest'])

    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datatrans.fieldwordcount': {
            'Meta': {'unique_together': "(('content_type', 'field'),)", 'object_name': 'FieldWordCount'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_words': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'datatrans.keyvalue': {
            'Meta': {'unique_together': "(('language', 'content_type', 'field', 'object_id', 'digest'),)", 'object_name': 'KeyValue'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'fuzzy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'datatrans.modelwordcount': {
            'Meta': {'object_name': 'ModelWordCount'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_words': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['datatrans']