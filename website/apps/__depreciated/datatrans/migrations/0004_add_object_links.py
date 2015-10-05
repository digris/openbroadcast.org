# encoding: utf-8
from collections import defaultdict

from south.v2 import DataMigration
from django.contrib.contenttypes.models import ContentType

from datatrans.models import make_digest, KeyValue
from datatrans.utils import get_registry


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."

        registry = get_registry()
        counts = defaultdict(lambda: [])

        for modelclass, fields in registry.items():
            ct = ContentType.objects.get_for_model(modelclass)
            for object in modelclass.objects.all():
                for field in fields.keys():
                    value = object.__dict__[field]
                    counts[value].append((object, field))
                    digest = make_digest(value)

                    done = {}

                    for kv in KeyValue.objects.filter(digest=digest).all():
                        if kv.object_id is None:
                            kv.content_object = object
                            kv.field = field
                            kv.save()
                        else:
                            if not kv.language in done:
                                KeyValue.objects.get_or_create(
                                    digest = kv.digest,
                                    language = kv.language,
                                    object_id = object.id,
                                    content_type_id = ct.id,
                                    field = field,
                                    defaults = { 'value': kv.value,
                                                 'edited': kv.edited,
                                                 'fuzzy': kv.fuzzy,
                                               }
                                )
                                done[kv.language] = 1

        # for value, uses in counts.items():
        #     if len(uses) > 1:
        #         print value, uses


    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datatrans.keyvalue': {
            'Meta': {'object_name': 'KeyValue'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'digest': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'field': ('django.db.models.fields.TextField', [], {}),
            'fuzzy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['datatrans']
