# -*- coding: utf-8 -*-
from platform_base.utils.check import FileOutputWrapper, check
from django.core.management.base import NoArgsCommand, CommandError


class CheckInstallation(NoArgsCommand):
    help = 'Checks your settings and environment'

    def handle_noargs(self, **options):
        if not check(FileOutputWrapper(self.stdout, self.stderr)):
            raise CommandError()
