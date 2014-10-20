import sys

from django.core.cache import cache
from django.test import TestCase
from django.utils import translation
from django.contrib.contenttypes.models import ContentType

from datatrans.models import KeyValue, make_digest


if len(sys.argv) > 1 and sys.argv[1] == 'test':
    # We need a model to translate. This is a bit hacky, see
    # http://code.djangoproject.com/ticket/7835
    from django.db import models

    class ModelToTranslate(models.Model):
        message = models.TextField()


class DatatransTests(TestCase):
    def setUp(self):
        self.nl = 'nl'
        self.en = 'en'
        self.message_en = 'Message in English'
        self.message_nl = 'Bericht in het Nederlands'
        self.field = 'message'
        self.instance = ModelToTranslate.objects.create(message=self.message_en)

    def test_default_values(self):
        value = KeyValue.objects.lookup(self.message_en, self.nl, self.instance, self.field)
        self.assertEqual(value, self.message_en)

        kv = KeyValue.objects.get_keyvalue(self.message_en, self.nl, self.instance, self.field)
        kv.value = self.message_nl
        kv.save()

        value = KeyValue.objects.lookup(self.message_en, self.nl, self.instance, self.field)
        self.assertEqual(value, self.message_en)

        kv.edited = True
        kv.save()

        value = KeyValue.objects.lookup(self.message_en, self.nl, self.instance, self.field)
        self.assertEqual(value, self.message_nl)

    def test_cache(self):
        digest = make_digest(self.message_en)
        type_id = ContentType.objects.get_for_model(self.instance.__class__).id
        cache_key = 'datatrans_%s_%s_%s_%s_%s' % (self.nl,
                                                  digest,
                                                  type_id,
                                                  self.instance.id,
                                                  self.field)

        self.assertEqual(cache.get(cache_key), None)

        translation.activate(self.nl)

        kv = KeyValue.objects.get_keyvalue(self.message_en, self.nl, self.instance, self.field)
        self.assertEqual(cache.get(cache_key).value, self.message_en)
        kv.value = self.message_nl
        kv.save()
        kv = KeyValue.objects.get_keyvalue(self.message_en, self.nl, self.instance, self.field)
        self.assertEqual(cache.get(cache_key).value, self.message_nl)
        kv.value = '%s2' % self.message_nl
        kv.save()
        self.assertEqual(cache.get(cache_key).value, '%s2' % self.message_nl)
        kv.delete()
        self.assertEqual(cache.get(cache_key), None)

    def test_fuzzy(self):
        kv = KeyValue.objects.get_keyvalue(self.message_en, self.nl, self.instance, self.field)
        kv.value = self.message_nl
        kv.edited = True
        kv.fuzzy = True
        kv.save()

        value = KeyValue.objects.lookup(self.message_en, self.nl, self.instance, self.field)
        self.assertEqual(value, self.message_nl)
