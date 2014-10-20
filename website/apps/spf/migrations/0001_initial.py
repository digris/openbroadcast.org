# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Request'
        db.create_table('spf_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('swp_id', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=12, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=12, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('spf', ['Request'])


    def backwards(self, orm):
        # Deleting model 'Request'
        db.delete_table('spf_request')


    models = {
        'spf.request': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Request'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'swp_id': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['spf']