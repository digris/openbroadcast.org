# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import logging

from django.http import HttpResponse
from django.views.generic import RedirectView, View
from django.core.urlresolvers import reverse
from django.views.static import serve
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.views import login
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import ugettext as _
from exceptions import ValueError
from BeautifulSoup import BeautifulSoup

DOCS_ROOT = getattr(settings, 'DOCS_ROOT', None)

class DocsRootSettingError(ValueError):
    pass



def process_document(path):

    html = open(path,'r').read()
    soup = BeautifulSoup(html)
    head = soup.find('head')
    body = soup.find('body')

    navigation = body.findAll("div", {"class": "related"})[0].findAll("ul")[0]
    toc = body.findAll("div", {"class": "sphinxsidebar"})[0].findAll("ul")[0]
    document = body.findAll("div", {"class": "document"})[0]

    return {
        'html': html,
        'head': str(head),
        'body': str(body),
        'navigation': str(navigation),
        'toc': str(toc),
        'document': str(document),
    }




class DocsRootView(RedirectView):
    """
    redirect root view to *index.html*
    """
    def get_redirect_url(self, **kwargs):
        return reverse('docs_documents', kwargs={'path': 'index.html'})


class DocsDocumentView(View):

    def get(self, request, path, **kwargs):

        if 'docs_root' in kwargs:
            docs_root = kwargs['docs_root']
        else:
            docs_root = DOCS_ROOT

        abs_path = os.path.join(docs_root, path)

        if not path.endswith('.html'):
            print 'path:     %s' % path
            return serve(request, path, docs_root, **kwargs)

        else:

            print 'path:     %s' % path
            print 'abs_path: %s' % abs_path

            #return serve(request, path, docs_root, **kwargs)


            elements = process_document(abs_path)

            return render(request, 'djangocms_sphinxdoc/base.html', {'elements': elements})

            #return HttpResponse(elements['body'])







#@decorator
def serve_docs(request, path, **kwargs):

    if 'docs_root' not in kwargs and not DOCS_ROOT:
        raise DocsRootSettingError('DOCS_ROOT setting value is incorrect: %s (must be a valid path)' % DOCS_ROOT)
    if 'docs_root' not in kwargs and DOCS_ROOT:
        kwargs['docs_root'] = DOCS_ROOT

    abs_path = os.path.join(DOCS_ROOT, path)
    soup = BeautifulSoup(open(abs_path,'r').read())

    body = soup.find('body')

    print body


    return serve(request, path, **kwargs)



