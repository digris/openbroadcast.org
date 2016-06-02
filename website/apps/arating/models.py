from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.utils.translation import ugettext as _

from base.models import TimestampedModel

VOTE_CHOICES = (
    (+1, '+1'),
    (-1, '-1'),
)

class Vote(TimestampedModel):

    vote = models.SmallIntegerField(choices=VOTE_CHOICES)
    user = models.ForeignKey(User, related_name="votes")

    # generic foreign key to the model being voted upon
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')


    class Meta:
        app_label = 'arating'
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        unique_together = (('user', 'content_type', 'object_id'),)

        permissions = (
            ('vote_for_user', 'Can vote in behalf of other user'),
        )


    def __unicode__(self):
        return '%s from %s on %s' % (self.get_vote_display(), self.user,
                                     self.content_object)


def post_save_vote(sender, **kwargs):
    obj = kwargs['instance']
    try:
        from pushy.util import pushy_custom
        pushy_custom(obj.content_object.get_api_url(), type='update')
    except Exception as e:
        pass

post_save.connect(post_save_vote, sender=Vote)