# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib.contenttypes.models import ContentType
from haystack import signals
from haystack.exceptions import NotHandled

class SearchIndexProcessor(signals.RealtimeSignalProcessor):



    def handle_save(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        update should be sent to & update the object on those backends.
        """
        using_backends = self.connection_router.for_write(instance=instance)

        for using in using_backends:
            try:
                index = self.connections[using].get_unified_index().get_index(sender)
                index.update_object(instance, using=using)

                print('updated index for {}'.format(instance))

            except NotHandled as e:
                pass
