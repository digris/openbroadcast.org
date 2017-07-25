# -*- coding: utf-8 -*-
import os
import sys
from split_settings.tools import optional, include

TESTING = sys.argv[1:2] == ['test']


if TESTING:
    site_settings = os.path.join(os.getcwd(), 'project/test_settings.py')
else:
    site_settings = os.path.join(os.getcwd(), 'project/local_settings.py')


# override site settings from path in environment
try:
    settings_path = os.environ['SETTINGS_PATH']
    if settings_path:
        site_settings = os.path.abspath(settings_path)

except KeyError:
    pass




include(
    'components/10-base.py',
    'components/11-apps.py',
    'components/12-identity.py',
    'components/13-credentials.py',
    'components/14-binaries.py',
    'components/20-media.py',
    'components/21-messaging.py',
    'components/30-template_cms.py',
    'components/99-depreciated.py',

    # via local_settings.py
    optional(site_settings),

    # via server based settings in etc (placed by ansible deployment tasks)
    optional('/etc/openbroadcast.org/application-settings.py'),
    optional('/etc/openbroadcast.org/application-secrets.py'),
    optional('/etc/openbroadcast.org/application-logging.py'),

    scope=locals()
)
