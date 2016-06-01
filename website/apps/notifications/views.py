# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from notifications.models import Notification

from .utils import slug2id


@login_required
def all(request):
    """
    Index page for authenticated user
    """
    return render(request, 'notifications/list.html', {
        'notifications': request.user.notifications.all()
    })


@login_required
def unread(request):
    return render(request, 'notifications/list.html', {
        'notifications': request.user.notifications.unread()
    })


@login_required
def mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()
    return redirect('notifications:all')


@login_required
def mark_as_read(request, slug=None):
    id = slug2id(slug)

    notification = get_object_or_404(Notification, recipient=request.user, id=id)
    notification.mark_as_read()

    next = request.REQUEST.get('next')

    if next:
        return redirect(next)

    return redirect('notifications:all')
