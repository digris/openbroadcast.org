# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ResourceMap'
        db.create_table('apiv1cache_resourcemap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=56, null=True)),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('v1_id', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('v2_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('v1_url', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('v2_url', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal('apiv1cache', ['ResourceMap'])


    def backwards(self, orm):
        # Deleting model 'ResourceMap'
        db.delete_table('apiv1cache_resourcemap')


    models = {
        'apiv1cache.resourcemap': {
            'Meta': {'object_name': 'ResourceMap'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '56', 'null': 'True'}),
            'v1_id': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'v1_url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'v2_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'v2_url': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['apiv1cache']