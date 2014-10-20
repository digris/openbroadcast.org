# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Backfeed'
        db.create_table(u'backfeed_backfeed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('backfeed', ['Backfeed'])


    def backwards(self, orm):
        # Deleting model 'Backfeed'
        db.delete_table(u'backfeed_backfeed')


    models = {
        'backfeed.backfeed': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Backfeed'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['backfeed']