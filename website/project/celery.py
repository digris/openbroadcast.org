from __future__ import absolute_import

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from django.conf import settings  # noqa

app = Celery("project")

app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# # setup celery 4.*
# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
#
# app = Celery('project')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
