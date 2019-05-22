# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.http import HttpResponseRedirect
from django.urls import reverse, resolve
from django.contrib import messages

# class RedirectIncompleteProfileMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#
#         if request.user.is_authenticated() and hasattr(request.user, 'profile') and not request.user.profile.profile_completed and (resolve(request.path_info).url_name != 'profile-edit'):
#
#             url = reverse('member:profile-edit', kwargs={'uuid': request.user.profile.uuid})
#             html = '''<p class="text-center">Please complete your Profile!</p>'''
#             messages.add_message(request, messages.INFO, html)
#
#             return HttpResponseRedirect(url)
