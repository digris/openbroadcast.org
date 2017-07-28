# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from djangocms_sphinxdoc.views import DocsRootView, serve_docs, DocsDocumentView

urlpatterns = [
    url(r'^$', DocsRootView.as_view(permanent=False), name='docs_root'),
    url(r'^genindex.html$', DocsRootView.as_view(permanent=False), name='docs_root'),
    url(r'^(?P<path>.*)$', DocsDocumentView.as_view(), name='docs_documents'),
]
