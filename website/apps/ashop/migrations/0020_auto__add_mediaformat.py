# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Mediaformat'
        db.create_table('ashop_mediaformat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ashop.Downloadmedia'])),
            ('format', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['alibrary.Format'])),
        ))
        db.send_create_signal('ashop', ['Mediaformat'])


    def backwards(self, orm):
        
        # Deleting model 'Mediaformat'
        db.delete_table('ashop_mediaformat')


    models = {
        'alibrary.artist': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Artist'},
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'artist_folder'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'artist_main_image'", 'null': 'True', 'to': "orm['filer.Image']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alibrary.Artist']", 'through': "orm['alibrary.ArtistMembership']", 'symmetrical': 'False'}),
            'multiple': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'professions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alibrary.Profession']", 'through': "orm['alibrary.ArtistProfessions']", 'symmetrical': 'False'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'alibrary.artistmembership': {
            'Meta': {'object_name': 'ArtistMembership'},
            'child': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'artist_child'", 'to': "orm['alibrary.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'artist_parent'", 'to': "orm['alibrary.Artist']"}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'artist_membership_profession'", 'null': 'True', 'to': "orm['alibrary.Profession']"})
        },
        'alibrary.artistprofessions': {
            'Meta': {'object_name': 'ArtistProfessions'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Profession']"})
        },
        'alibrary.format': {
            'Meta': {'ordering': "('format', 'version')", 'object_name': 'Format'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'base'", 'max_length': '10'})
        },
        'alibrary.label': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Label'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_main': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'label_folder'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labelcode': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'label_children'", 'null': 'True', 'to': "orm['alibrary.Label']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'fcd86798-a040-4e64-b79e-2f4942572ee1'", 'max_length': '36'})
        },
        'alibrary.license': {
            'Meta': {'ordering': "('name',)", 'object_name': 'License'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'license_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'license_children'", 'null': 'True', 'to': "orm['alibrary.License']"}),
            'restricted': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'028e8898-b3aa-4ee9-bddd-b61a7467a988'", 'max_length': '36'})
        },
        'alibrary.media': {
            'Meta': {'ordering': "('tracknumber',)", 'object_name': 'Media'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media_artist'", 'null': 'True', 'to': "orm['alibrary.Artist']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['alibrary.Profession']", 'null': 'True', 'through': "orm['alibrary.MediaExtraartists']", 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media_folder'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isrc': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media_license'", 'null': 'True', 'to': "orm['alibrary.License']"}),
            'lock': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '1'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media_master'", 'null': 'True', 'to': "orm['filer.Audio']"}),
            'mediatype': ('django.db.models.fields.CharField', [], {'default': "'track'", 'max_length': '12'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'processed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '2'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'media_release'", 'to': "orm['alibrary.Release']"}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False', 'db_index': 'True'}),
            'tracknumber': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '12'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'})
        },
        'alibrary.mediaextraartists': {
            'Meta': {'object_name': 'MediaExtraartists'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extraartist_artist'", 'to': "orm['alibrary.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extraartist_media'", 'to': "orm['alibrary.Media']"}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media_extraartist_profession'", 'null': 'True', 'to': "orm['alibrary.Profession']"})
        },
        'alibrary.profession': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Profession'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_listing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'alibrary.release': {
            'Meta': {'ordering': "('releasedate',)", 'object_name': 'Release'},
            'catalognumber': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['alibrary.Artist']", 'null': 'True', 'through': "orm['alibrary.ReleaseExtraartists']", 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_folder'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'release_label'", 'to': "orm['alibrary.Label']"}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_main_image'", 'null': 'True', 'to': "orm['filer.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'placeholder_1': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'pressings': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '12'}),
            'releasedate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'releasetype': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '12'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'alibrary.releaseextraartists': {
            'Meta': {'object_name': 'ReleaseExtraartists'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'release_extraartist_artist'", 'to': "orm['alibrary.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_extraartist_profession'", 'null': 'True', 'to': "orm['alibrary.Profession']"}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'release_extraartist_release'", 'to': "orm['alibrary.Release']"})
        },
        'ashop.downloadmedia': {
            'Meta': {'ordering': "['name']", 'object_name': 'Downloadmedia', '_ormbases': ['shop.Product']},
            'media': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediaproduct'", 'to': "orm['alibrary.Media']"}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['shop.Product']", 'unique': 'True', 'primary_key': 'True'})
        },
        'ashop.downloadrelease': {
            'Meta': {'ordering': "['name']", 'object_name': 'Downloadrelease', '_ormbases': ['ashop.Releaseproduct']},
            'releaseproduct_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ashop.Releaseproduct']", 'unique': 'True', 'primary_key': 'True'})
        },
        'ashop.hardwarerelease': {
            'Meta': {'ordering': "['name']", 'object_name': 'Hardwarerelease', '_ormbases': ['ashop.Releaseproduct']},
            'circulation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'needs_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'releaseproduct_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ashop.Releaseproduct']", 'unique': 'True', 'primary_key': 'True'}),
            'weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'ashop.mediaformat': {
            'Meta': {'object_name': 'Mediaformat'},
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Format']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ashop.Downloadmedia']"})
        },
        'ashop.releaseproduct': {
            'Meta': {'ordering': "['name']", 'object_name': 'Releaseproduct', '_ormbases': ['shop.Product']},
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['shop.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'releaseproduct'", 'to': "orm['alibrary.Release']"})
        },
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
        'filer.audio': {
            'Meta': {'object_name': 'Audio', '_ormbases': ['filer.File']},
            'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['filer.File']", 'unique': 'True', 'primary_key': 'True'})
        },
        'filer.file': {
            'Meta': {'object_name': 'File'},
            '_file_size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'all_files'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'has_all_mandatory_data': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'original_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_files'", 'null': 'True', 'to': "orm['auth.User']"}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_filer.file_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'sha1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.folder': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Folder'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'filer_owned_folders'", 'null': 'True', 'to': "orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['filer.Folder']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'filer.image': {
            'Meta': {'object_name': 'Image', '_ormbases': ['filer.File']},
            '_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'default_alt_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'default_caption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'file_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['filer.File']", 'unique': 'True', 'primary_key': 'True'}),
            'must_always_publish_author_credit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'must_always_publish_copyright': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_location': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'shop.product': {
            'Meta': {'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_shop.product_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'False', 'db_index': 'True'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '12', 'decimal_places': '2'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['ashop']
