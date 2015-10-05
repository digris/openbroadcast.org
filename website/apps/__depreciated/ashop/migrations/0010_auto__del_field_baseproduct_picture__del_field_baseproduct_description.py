# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Baseproduct.picture'
        db.delete_column('ashop_baseproduct', 'picture_id')

        # Deleting field 'Baseproduct.description'
        db.delete_column('ashop_baseproduct', 'description')

        # Deleting field 'Baseproduct.subline'
        db.delete_column('ashop_baseproduct', 'subline')

        # Deleting field 'Baseproduct.picture_listing'
        db.delete_column('ashop_baseproduct', 'picture_listing_id')

        # Deleting field 'Baseproduct.excerpt'
        db.delete_column('ashop_baseproduct', 'excerpt')


    def backwards(self, orm):
        
        # Adding field 'Baseproduct.picture'
        db.add_column('ashop_baseproduct', 'picture', self.gf('django.db.models.fields.related.ForeignKey')(related_name='baseproduct_picture', null=True, to=orm['filer.Image'], blank=True), keep_default=False)

        # Adding field 'Baseproduct.description'
        db.add_column('ashop_baseproduct', 'description', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Baseproduct.subline'
        db.add_column('ashop_baseproduct', 'subline', self.gf('django.db.models.fields.CharField')(default='none', max_length=255), keep_default=False)

        # Adding field 'Baseproduct.picture_listing'
        db.add_column('ashop_baseproduct', 'picture_listing', self.gf('django.db.models.fields.related.ForeignKey')(related_name='baseproduct_picture_listing', null=True, to=orm['filer.Image'], blank=True), keep_default=False)

        # Adding field 'Baseproduct.excerpt'
        db.add_column('ashop_baseproduct', 'excerpt', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    models = {
        'ashop.baseproduct': {
            'Meta': {'ordering': "['name']", 'object_name': 'Baseproduct', '_ormbases': ['shop.Product']},
            'needs_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['shop.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ashop.book': {
            'Meta': {'ordering': "['author']", 'object_name': 'Book', '_ormbases': ['shop.Product']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['shop.Product']", 'unique': 'True', 'primary_key': 'True'})
        },
        'ashop.singleproduct': {
            'Meta': {'object_name': 'SingleProduct', 'db_table': "'cmsplugin_singleproduct'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ashop.Baseproduct']"}),
            'style': ('django.db.models.fields.CharField', [], {'default': "'l'", 'max_length': '24'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shop.product': {
            'Meta': {'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_shop.product_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '12', 'decimal_places': '2'})
        }
    }

    complete_apps = ['ashop']
