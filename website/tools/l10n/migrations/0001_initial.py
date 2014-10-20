# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Country'
        db.create_table('l10n_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso2_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('printable_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('iso3_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('numcode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('continent', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('admin_area', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal('l10n', ['Country'])

        # Adding model 'AdminArea'
        db.create_table('l10n_adminarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['l10n.Country'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('l10n', ['AdminArea'])

        # Adding model 'Address'
        db.create_table('l10n_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_shipping', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='shipping_address', unique=True, null=True, to=orm['auth.User'])),
            ('user_billing', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='billing_address', unique=True, null=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['l10n.AdminArea'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['l10n.Country'])),
        ))
        db.send_create_signal('l10n', ['Address'])


    def backwards(self, orm):
        
        # Deleting model 'Country'
        db.delete_table('l10n_country')

        # Deleting model 'AdminArea'
        db.delete_table('l10n_adminarea')

        # Deleting model 'Address'
        db.delete_table('l10n_address')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'l10n.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['l10n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['l10n.AdminArea']"}),
            'user_billing': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'billing_address'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'user_shipping': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'shipping_address'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'l10n.adminarea': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AdminArea'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['l10n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'l10n.country': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Country'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'admin_area': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'numcode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['l10n']
