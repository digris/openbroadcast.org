# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'KeyValue'
        db.create_table('datatrans_keyvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('digest', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('edited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fuzzy', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('datatrans', ['KeyValue'])


    def backwards(self, orm):
        
        # Deleting model 'KeyValue'
        db.delete_table('datatrans_keyvalue')


    models = {
        'datatrans.keyvalue': {
            'Meta': {'object_name': 'KeyValue'},
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fuzzy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['datatrans']
