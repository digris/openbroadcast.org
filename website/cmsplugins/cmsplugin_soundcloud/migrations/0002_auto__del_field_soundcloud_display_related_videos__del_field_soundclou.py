# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Soundcloud.display_related_videos'
        db.delete_column('cmsplugin_soundcloud', 'display_related_videos')

        # Deleting field 'Soundcloud.height'
        db.delete_column('cmsplugin_soundcloud', 'height')

        # Deleting field 'Soundcloud.border'
        db.delete_column('cmsplugin_soundcloud', 'border')

        # Deleting field 'Soundcloud.allow_fullscreen'
        db.delete_column('cmsplugin_soundcloud', 'allow_fullscreen')

        # Deleting field 'Soundcloud.high_quality'
        db.delete_column('cmsplugin_soundcloud', 'high_quality')

        # Deleting field 'Soundcloud.video_id'
        db.delete_column('cmsplugin_soundcloud', 'video_id')

        # Deleting field 'Soundcloud.width'
        db.delete_column('cmsplugin_soundcloud', 'width')

        # Deleting field 'Soundcloud.loop'
        db.delete_column('cmsplugin_soundcloud', 'loop')

        # Adding field 'Soundcloud.track_id'
        db.add_column('cmsplugin_soundcloud', 'track_id', self.gf('django.db.models.fields.CharField')(default=0, max_length=60), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Soundcloud.display_related_videos'
        db.add_column('cmsplugin_soundcloud', 'display_related_videos', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Soundcloud.height'
        db.add_column('cmsplugin_soundcloud', 'height', self.gf('django.db.models.fields.IntegerField')(default=344), keep_default=False)

        # Adding field 'Soundcloud.border'
        db.add_column('cmsplugin_soundcloud', 'border', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Soundcloud.allow_fullscreen'
        db.add_column('cmsplugin_soundcloud', 'allow_fullscreen', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'Soundcloud.high_quality'
        db.add_column('cmsplugin_soundcloud', 'high_quality', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Soundcloud.video_id'
        db.add_column('cmsplugin_soundcloud', 'video_id', self.gf('django.db.models.fields.CharField')(default=0, max_length=60), keep_default=False)

        # Adding field 'Soundcloud.width'
        db.add_column('cmsplugin_soundcloud', 'width', self.gf('django.db.models.fields.IntegerField')(default=425), keep_default=False)

        # Adding field 'Soundcloud.loop'
        db.add_column('cmsplugin_soundcloud', 'loop', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'Soundcloud.track_id'
        db.delete_column('cmsplugin_soundcloud', 'track_id')


    models = {
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
        'cmsplugin_soundcloud.soundcloud': {
            'Meta': {'object_name': 'Soundcloud', 'db_table': "'cmsplugin_soundcloud'", '_ormbases': ['cms.CMSPlugin']},
            'autoplay': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'track_id': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        }
    }

    complete_apps = ['cmsplugin_soundcloud']
