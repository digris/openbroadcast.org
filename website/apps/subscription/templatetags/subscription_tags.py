from django import template
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from subscription.models import Newsletter

register = template.Library()

DEFAULT_LIST_ID = getattr(settings, 'SUBSCRIPTION_DEFAULT_LIST_ID', 1)
DEBUG = getattr(settings, 'DEBUG', False)

@register.inclusion_tag('subscription/templatetags/subscription_form.html', takes_context=True)
def subscription_form(context, list_id=DEFAULT_LIST_ID):

    if list_id:
        try:
            newsletter = Newsletter.objects.get(id=list_id)
            context['newsletter'] = newsletter
            context['list_id'] = list_id
        except Exception as e:
            if DEBUG:
                context['error'] = u'%s' % e

    return context
