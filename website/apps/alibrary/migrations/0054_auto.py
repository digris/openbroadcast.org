# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field payparts on 'Playlist'
        db.delete_table('alibrary_playlist_payparts')


    def backwards(self, orm):
        # Adding M2M table for field payparts on 'Playlist'
        db.create_table('alibrary_playlist_payparts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('playlist', models.ForeignKey(orm['alibrary.playlist'], null=False)),
            ('daypart', models.ForeignKey(orm['alibrary.daypart'], null=False))
        ))
        db.create_unique('alibrary_playlist_payparts', ['playlist_id', 'daypart_id'])


    models = {
        'actstream.action': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Action'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_object'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'to': "orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'alibrary.apilookup': {
            'Meta': {'ordering': "('created',)", 'object_name': 'APILookup'},
            'api_data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'processed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '2'}),
            'provider': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50'}),
            'ressource_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'alibrary.artist': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Artist'},
            'aliases': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'aliases_rel_+'", 'null': 'True', 'to': "orm['alibrary.Artist']"}),
            'biography': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disable_link': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'artist_folder'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['filer.Folder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legacy_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'listed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'artist_main_image'", 'null': 'True', 'to': "orm['filer.Image']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alibrary.Artist']", 'through': "orm['alibrary.ArtistMembership']", 'symmetrical': 'False'}),
            'migrated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'placeholder_1': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'professions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['alibrary.Profession']", 'through': "orm['alibrary.ArtistProfessions']", 'symmetrical': 'False'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True'}),
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
        'alibrary.artistplugin': {
            'Meta': {'object_name': 'ArtistPlugin', 'db_table': "'cmsplugin_artistplugin'", '_ormbases': ['cms.CMSPlugin']},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Artist']"}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'})
        },
        'alibrary.artistprofessions': {
            'Meta': {'object_name': 'ArtistProfessions'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Profession']"})
        },
        'alibrary.daypart': {
            'Meta': {'ordering': "('day',)", 'object_name': 'Daypart'},
            'day': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '1', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_end': ('django.db.models.fields.TimeField', [], {}),
            'time_start': ('django.db.models.fields.TimeField', [], {})
        },
        'alibrary.format': {
            'Meta': {'ordering': "('format', 'version')", 'object_name': 'Format'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default_price': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'max_length': '6', 'null': 'True', 'blank': 'True'}),
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
            'legacy_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'migrated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'label_children'", 'null': 'True', 'to': "orm['alibrary.Label']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'alibrary.license': {
            'Meta': {'ordering': "('name',)", 'object_name': 'License'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'legacy_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'migrated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'license_children'", 'null': 'True', 'to': "orm['alibrary.License']"}),
            'restricted': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'559e3a89-07f9-4406-9a0e-e2754fb47404'", 'max_length': '36'})
        },
        'alibrary.licensetranslation': {
            'Meta': {'ordering': "('language_code',)", 'unique_together': "(('language_code', 'master'),)", 'object_name': 'LicenseTranslation', 'db_table': "'alibrary_license_translation'"},
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'blank': 'True'}),
            'license_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': "orm['alibrary.License']"}),
            'name_translated': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'alibrary.media': {
            'Meta': {'ordering': "('tracknumber',)", 'object_name': 'Media'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media_artist'", 'null': 'True', 'to': "orm['alibrary.Artist']"}),
            'base_bitrate': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'base_duration': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'base_filesize': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'base_format': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'base_samplerate': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'conversion_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'echoprint_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '2'}),
            'extra_artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['alibrary.Profession']", 'null': 'True', 'through': "orm['alibrary.MediaExtraartists']", 'blank': 'True'}),
            'folder': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isrc': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'legacy_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media_license'", 'null': 'True', 'to': "orm['alibrary.License']"}),
            'lock': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '1'}),
            'master': ('django.db.models.fields.files.FileField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'master_sha1': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'mediatype': ('django.db.models.fields.CharField', [], {'default': "'track'", 'max_length': '12'}),
            'migrated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'processed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '2'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media_release'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['alibrary.Release']"}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True'}),
            'tracknumber': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '12'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'alibrary.mediaextraartists': {
            'Meta': {'object_name': 'MediaExtraartists'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extraartist_artist'", 'to': "orm['alibrary.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'extraartist_media'", 'to': "orm['alibrary.Media']"}),
            'profession': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'media_extraartist_profession'", 'null': 'True', 'to': "orm['alibrary.Profession']"})
        },
        'alibrary.mediaformat': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Mediaformat'},
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_listing': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'alibrary.mediaplugin': {
            'Meta': {'object_name': 'MediaPlugin', 'db_table': "'cmsplugin_mediaplugin'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'headline': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Media']"})
        },
        'alibrary.playlist': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Playlist'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'd_tags': ('tagging.fields.TagField', [], {'null': 'True'}),
            'description': ('lib.fields.extra.MarkdownTextField', [], {'null': 'True', 'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '12', 'null': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['alibrary.Media']", 'null': 'True', 'through': "orm['alibrary.PlaylistMedia']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '12', 'null': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'alibrary.playlistmedia': {
            'Meta': {'object_name': 'PlaylistMedia'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cue_in': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '12'}),
            'cue_out': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '12'}),
            'fade_in': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '12'}),
            'fade_out': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Media']"}),
            'playlist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Playlist']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '12'})
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
        'alibrary.relation': {
            'Meta': {'ordering': "('url',)", 'unique_together': "(('service', 'content_type', 'object_id'),)", 'object_name': 'Relation'},
            'action': ('django.db.models.fields.CharField', [], {'default': "'information'", 'max_length': '50'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'default': "'generic'", 'max_length': '50'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '512'})
        },
        'alibrary.release': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Release'},
            'asin': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'catalognumber': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'cover_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_cover_image'", 'null': 'True', 'to': "orm['filer.Image']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'd_tags': ('tagging.fields.TagField', [], {'null': 'True'}),
            'description': ('lib.fields.extra.MarkdownTextField', [], {'null': 'True', 'blank': 'True'}),
            'description_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['alibrary.Artist']", 'null': 'True', 'through': "orm['alibrary.ReleaseExtraartists']", 'blank': 'True'}),
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_folder'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['filer.Folder']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_label'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['alibrary.Label']"}),
            'legacy_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_license'", 'null': 'True', 'to': "orm['alibrary.License']"}),
            'main_format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Mediaformat']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'main_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_main_image'", 'null': 'True', 'to': "orm['filer.Image']"}),
            'migrated': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_owner'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'placeholder_1': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'pressings': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '12'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'release_publisher'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['auth.User']"}),
            'release_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'releasedate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'releasestatus': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'releasetype': ('django.db.models.fields.CharField', [], {'default': "'other'", 'max_length': '12'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True'}),
            'totaltracks': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
        'alibrary.releaseplugin': {
            'Meta': {'object_name': 'ReleasePlugin', 'db_table': "'cmsplugin_releaseplugin'", '_ormbases': ['cms.CMSPlugin']},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['alibrary.Release']"})
        },
        'alibrary.releaserelations': {
            'Meta': {'object_name': 'ReleaseRelations'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'release_relation_relation'", 'to': "orm['alibrary.Relation']"}),
            'release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'release_relation_release'", 'to': "orm['alibrary.Release']"})
        },
        'arating.vote': {
            'Meta': {'unique_together': "(('user', 'content_type', 'object_id'),)", 'object_name': 'Vote'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote': ('django.db.models.fields.SmallIntegerField', [], {})
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        }
    }

    complete_apps = ['alibrary']