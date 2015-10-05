# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ModelWordCount'
        db.create_table('datatrans_modelwordcount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_words', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], unique=True)),
        ))
        db.send_create_signal('datatrans', ['ModelWordCount'])

        # Adding model 'FieldWordCount'
        db.create_table('datatrans_fieldwordcount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_words', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
        ))
        db.send_create_signal('datatrans', ['FieldWordCount'])

        # Adding unique constraint on 'FieldWordCount', fields ['content_type', 'field']
        db.create_unique('datatrans_fieldwordcount', ['content_type_id', 'field'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FieldWordCount', fields ['content_type', 'field']
        db.delete_unique('datatrans_fieldwordcount', ['content_type_id', 'field'])

        # Deleting model 'ModelWordCount'
        db.delete_table('datatrans_modelwordcount')

        # Deleting model 'FieldWordCount'
        db.delete_table('datatrans_fieldwordcount')


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
            'Meta': {'unique_together': "(('digest', 'language'),)", 'object_name': 'KeyValue'},
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fuzzy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
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
