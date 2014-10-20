# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RelatedContent'
        db.create_table('genericrelations_relatedcontent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('parent_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_test_link', to=orm['contenttypes.ContentType'])),
            ('parent_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('genericrelations', ['RelatedContent'])


    def backwards(self, orm):
        
        # Deleting model 'RelatedContent'
        db.delete_table('genericrelations_relatedcontent')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'genericrelations.relatedcontent': {
            'Meta': {'object_name': 'RelatedContent'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'parent_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_test_link'", 'to': "orm['contenttypes.ContentType']"}),
            'parent_object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['genericrelations']
