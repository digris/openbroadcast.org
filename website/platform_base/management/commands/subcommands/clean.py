# -*- coding: utf-8 -*-
import sys
from django.core.management.base import NoArgsCommand, CommandError
from django.db.models.loading import get_model
from tqdm import tqdm


class DeleteOrphanedTags(NoArgsCommand):
    help = 'Telete orphaned Tags (resp. TaggedItems)'

    def handle_noargs(self, **options):
        from tagging.models import TaggedItem
        to_delete = []
        tagged_items = TaggedItem.objects.all().nocache()
        for ti in tqdm(tagged_items):
            if not ti.object:
                to_delete.append(ti.pk)

        print 'Total tagged items:    {}'.format(tagged_items.count())
        print 'Orphaned tagged items: {}'.format(len(to_delete))

        TaggedItem.objects.filter(pk__in=to_delete).delete()
