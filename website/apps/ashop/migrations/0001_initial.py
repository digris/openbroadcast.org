# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Book'
        db.create_table('ashop_book', (
            ('product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['shop.Product'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('ashop', ['Book'])

        # Adding model 'Baseproduct'
        db.create_table('ashop_baseproduct', (
            ('product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['shop.Product'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('ashop', ['Baseproduct'])


    def backwards(self, orm):
        
        # Deleting model 'Book'
        db.delete_table('ashop_book')

        # Deleting model 'Baseproduct'
        db.delete_table('ashop_baseproduct')


    models = {
        'ashop.baseproduct': {
            'Meta': {'ordering': "['author']", 'object_name': 'Baseproduct', '_ormbases': ['shop.Product']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['shop.Product']", 'unique': 'True', 'primary_key': 'True'})
        },
        'ashop.book': {
            'Meta': {'ordering': "['author']", 'object_name': 'Book', '_ormbases': ['shop.Product']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['shop.Product']", 'unique': 'True', 'primary_key': 'True'})
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
