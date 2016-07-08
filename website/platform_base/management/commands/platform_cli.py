# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .subcommands.base import SubcommandsCommand
from .subcommands.check import CheckInstallation
from .subcommands.reset import ResetDatabase
from .subcommands.clean import DeleteOrphanedTags
from .subcommands.crawl import MBCrawlerCommand
from .subcommands.clean_assets import CleanAssets
from django.core.management.base import BaseCommand
from optparse import make_option



class Command(SubcommandsCommand):

    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', default=True,
        help='Tells platform to NOT prompt the user for input of any kind. '),
    )

    args = '<subcommand>'

    command_name = 'platform'

    subcommands = {
        'check': CheckInstallation,
        'reset': ResetDatabase,
        'delete_orphaned_tags': DeleteOrphanedTags,
        'crawl_mb': MBCrawlerCommand,
        'clean_assets': CleanAssets,
    }

    @property
    def help(self):
        lines = ['django CMS command line interface.', '', 'Available subcommands:']
        for subcommand in sorted(self.subcommands.keys()):
            lines.append('  %s' % subcommand)
        lines.append('')
        lines.append('Use `manage.py platform <subcommand> --help` for help about subcommands')
        return '\n'.join(lines)
