# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'KeyValue', fields ['language', 'digest']
        try:
            db.delete_unique('datatrans_keyvalue', ['language', 'digest'])
        except ValueError:
            print "  WARNING: current index didn't exist"

        # Adding field 'KeyValue.content_type'
        db.add_column('datatrans_keyvalue', 'content_type', self.gf('django.db.models.fields.related.ForeignKey')(default=None, null=True, to=orm['contenttypes.ContentType']), keep_default=False)

        # Adding field 'KeyValue.object_id'
        db.add_column('datatrans_keyvalue', 'object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, null=True), keep_default=False)

        # Adding field 'KeyValue.field'
        db.add_column('datatrans_keyvalue', 'field', self.gf('django.db.models.fields.TextField')(default=""), keep_default=False)

    def backwards(self, orm):
        
        # Deleting field 'KeyValue.content_type'
        db.delete_column('datatrans_keyvalue', 'content_type_id')

        # Deleting field 'KeyValue.object_id'
        db.delete_column('datatrans_keyvalue', 'object_id')

        # Deleting field 'KeyValue.field'
        db.delete_column('datatrans_keyvalue', 'field')

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
        'datatrans.keyvalue': {
            'Meta': {'object_name': 'KeyValue'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'field': ('django.db.models.fields.TextField', [], {}),
            'fuzzy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['datatrans']
