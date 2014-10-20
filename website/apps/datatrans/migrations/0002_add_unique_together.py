# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    depends_on = (
        ("datatrans", "0001a_remove_duplicates"),
    )

    def forwards(self, orm):
        
        # Adding unique constraint on 'KeyValue', fields ['language', 'digest']
        db.create_unique('datatrans_keyvalue', ['language', 'digest'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'KeyValue', fields ['language', 'digest']
        db.delete_unique('datatrans_keyvalue', ['language', 'digest'])


    models = {
        'datatrans.keyvalue': {
            'Meta': {'unique_together': "(('digest', 'language'),)", 'object_name': 'KeyValue'},
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'fuzzy': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['datatrans']
