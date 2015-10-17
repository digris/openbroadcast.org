from split_settings.tools import optional, include
import os

include(
    'components/base.py',
    'components/media.py',
    'components/template_cms.py',

    os.path.join(os.getcwd(), 'project/local_settings.py'),
    scope=locals()
)
