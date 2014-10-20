# encoding: utf-8
from collections import defaultdict

from south.v2 import DataMigration

class Migration(DataMigration):

    depends_on = (
        ("datatrans", "0001_initial"),
    )

    def forwards(self, orm):
        "Write your forwards methods here."

        kv_map = defaultdict(lambda: [])

        for kv in orm.KeyValue.objects.all():
            key = (kv.language, kv.digest)
            kv_map[key].append(kv)

        for (language, digest), kv_list in kv_map.items():
            if len(kv_list) == 1:
                continue

            kv_list.sort(key=lambda kv: kv.id)

            for kv in kv_list[:-1]:
                print 'Deleting KeyValue', kv.id
                kv.delete()


    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'datatrans.keyvalue': {
            'Meta': {'object_name': 'KeyValue'},
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fuzzy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['datatrans']

