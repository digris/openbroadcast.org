# -*- coding: utf-8 -*-
import re
import locale
import sys
import subprocess
from datetime import datetime
import os
from django.conf import settings
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.inclusion_tag('lib/templatetags/version_by_git.html', takes_context=True)
def version_by_git(context):

    commit, timestamp = parse_git_changelog()

    try:
        install_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(settings.BASE_DIR, 'changelog.txt')))
    except Exception, e:
        print e
        install_time = None

    context.update({
        'commit': commit,
        'timestamp': timestamp,
        'install_time': install_time,
    })

    return context



@register.inclusion_tag('lib/templatetags/locale_info.html', takes_context=True)
def locale_info(context):

    loc_info = {
        'loc_loc': locale.getlocale(),
        'loc_def': locale.getdefaultlocale(),
        'sys_fenc': sys.getfilesystemencoding(),
    }

    context.update({
        'locale_info': loc_info,
    })

    return context




def parse_git_changelog():

    try:

        log = subprocess.Popen("git log -n 1",
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in iter(log.stdout.readline,''):
            line = line.rstrip()
            if line[0:6] == 'commit':
                commit = line[7:].strip()
            if line[0:4] == 'Date':
                timestamp = line[7:].strip()
                # timestamp format:
                # Tue Oct 21 09:37:12 2014 +0200
                # %a  %b  %w %H:%M:%S %Y
                timestamp = datetime.strptime(line[8:].split(' +')[0], '%a %b %d %H:%M:%S %Y')
                break

        return commit, timestamp

    except Exception, e:
        print e
        return None, None
