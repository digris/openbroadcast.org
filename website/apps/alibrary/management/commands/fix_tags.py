#-*- coding: utf-8 -*-
import logging
import subprocess
from django.conf import settings
from django.core.management.base import NoArgsCommand


class CountryTagFix(object):
    def __init__(self, * args, **kwargs):
        self.verbosity = int(kwargs.get('verbosity', 1))

    def run(self):

        from tagging.models import TaggedItem

        sql_insert = """INSERT INTO `tagging_taggeditem` (`id`, `tag_id`, `content_type_id`, `object_id`) VALUES (NULL, '{tag_id}', '{ct_id}', '{obj_id}');"""


        tis = TaggedItem.objects.filter(tag_id=27635)

        for ti in tis:
            if ti.object:
                print sql_insert.format(tag_id=27635, ct_id=ti.content_type.pk, obj_id=ti.object_id)






        

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        tag_fix = CountryTagFix(**options)
        tag_fix.run()
