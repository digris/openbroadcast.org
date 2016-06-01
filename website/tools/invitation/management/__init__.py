from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User
from invitation import models


def create_stats_for_existing_users(sender, **kwargs):
    """
    Create `InvitationStats` objects for all users after a `sycndb`

    """
    count = 0
    for user in User.objects.filter(invitation_stats__isnull=True):
        models.InvitationStats.objects.create(user=user)
        count += 1
    if count > 0:
        print "Created InvitationStats for %s existing Users" % count


post_syncdb.connect(create_stats_for_existing_users, sender=models)
