# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FAQCateqory'
        db.create_table('faq_faqcateqory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('faq', ['FAQCateqory'])

        # Adding model 'FAQ'
        db.create_table('faq_faq', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('answer', self.gf('django.db.models.fields.TextField')()),
            ('weight', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=12)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['faq.FAQCateqory'], null=True, blank=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('faq', ['FAQ'])

        # Adding model 'FAQPlugin'
        db.create_table('cmsplugin_faqplugin', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('faq', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['faq.FAQ'])),
        ))
        db.send_create_signal('faq', ['FAQPlugin'])

        # Adding model 'FAQListPlugin'
        db.create_table('cmsplugin_faqlistplugin', (
            ('cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['faq.FAQCateqory'], null=True, blank=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=7)),
        ))
        db.send_create_signal('faq', ['FAQListPlugin'])


    def backwards(self, orm):
        # Deleting model 'FAQCateqory'
        db.delete_table('faq_faqcateqory')

        # Deleting model 'FAQ'
        db.delete_table('faq_faq')

        # Deleting model 'FAQPlugin'
        db.delete_table('cmsplugin_faqplugin')

        # Deleting model 'FAQListPlugin'
        db.delete_table('cmsplugin_faqlistplugin')


    models = {
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'faq.faq': {
            'Meta': {'object_name': 'FAQ'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faq.FAQCateqory']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '12'})
        },
        'faq.faqcateqory': {
            'Meta': {'object_name': 'FAQCateqory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'faq.faqlistplugin': {
            'Meta': {'object_name': 'FAQListPlugin', 'db_table': "'cmsplugin_faqlistplugin'", '_ormbases': ['cms.CMSPlugin']},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faq.FAQCateqory']", 'null': 'True', 'blank': 'True'}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        },
        'faq.faqplugin': {
            'Meta': {'object_name': 'FAQPlugin', 'db_table': "'cmsplugin_faqplugin'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'faq': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faq.FAQ']"})
        }
    }

    complete_apps = ['faq']