# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Link.title'
        db.alter_column('user_links', 'title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))
        # Deleting field 'Profile.mugshot'
        db.delete_column('user_profiles', 'mugshot')

        # Adding field 'Profile.image'
        db.add_column('user_profiles', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Profile.city'
        db.alter_column('user_profiles', 'city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Profile.zip'
        db.alter_column('user_profiles', 'zip', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

        # Changing field 'Profile.mobile'
        db.alter_column('user_profiles', 'mobile', self.gf('phonenumber_field.modelfields.PhoneNumberField')(max_length=128, null=True))

        # Changing field 'Profile.address2'
        db.alter_column('user_profiles', 'address2', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Profile.state'
        db.alter_column('user_profiles', 'state', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Profile.address1'
        db.alter_column('user_profiles', 'address1', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Profile.country'
        db.alter_column('user_profiles', 'country', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Link.title'
        raise RuntimeError("Cannot reverse this migration. 'Link.title' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Profile.mugshot'
        raise RuntimeError("Cannot reverse this migration. 'Profile.mugshot' and its values cannot be restored.")
        # Deleting field 'Profile.image'
        db.delete_column('user_profiles', 'image')


        # Changing field 'Profile.city'
        db.alter_column('user_profiles', 'city', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'Profile.zip'
        db.alter_column('user_profiles', 'zip', self.gf('django.db.models.fields.CharField')(default='', max_length=10))

        # Changing field 'Profile.mobile'
        db.alter_column('user_profiles', 'mobile', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(default='', max_length=20))

        # Changing field 'Profile.address2'
        db.alter_column('user_profiles', 'address2', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'Profile.state'
        db.alter_column('user_profiles', 'state', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'Profile.address1'
        db.alter_column('user_profiles', 'address1', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

        # Changing field 'Profile.country'
        db.alter_column('user_profiles', 'country', self.gf('django.db.models.fields.CharField')(default='', max_length=100))

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
        'profiles.link': {
            'Meta': {'object_name': 'Link', 'db_table': "'user_links'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Profile']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'profiles.mobileprovider': {
            'Meta': {'object_name': 'MobileProvider', 'db_table': "'user_mobile_providers'"},
            'domain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile', 'db_table': "'user_profiles'"},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('lib.fields.extra.MarkdownTextField', [], {'null': 'True', 'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mobile': ('phonenumber_field.modelfields.PhoneNumberField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'profiles.service': {
            'Meta': {'object_name': 'Service', 'db_table': "'user_services'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Profile']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.ServiceType']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.servicetype': {
            'Meta': {'object_name': 'ServiceType', 'db_table': "'user_service_types'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['profiles']