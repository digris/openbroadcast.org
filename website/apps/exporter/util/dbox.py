import logging

from celery.task import task
from social_auth.models import UserSocialAuth
from dropbox import client, session

import settings

log = logging.getLogger(__name__)

USE_CELERYD = True

class Synchronizer(object):


    def __init__(self, user):

        log.debug('initializing dropbox connection for: %s' % user)
        self.dbox_client = None

        # Get Access Token and Secret
        try:
            social_user = UserSocialAuth.objects.get(user=user, provider='dropbox')
        except UserSocialAuth.DoesNotExist:
            social_user = None

        if social_user:
            try:
                token = social_user.tokens['access_token'].split('&')[0].split('=')[1]
                secret = social_user.tokens['access_token'].split('&')[1].split('=')[1]

                # Set Access Token on Session
                dbox_session = session.DropboxSession(settings.DROPBOX_APP_ID,
                                                      settings.DROPBOX_API_SECRET,
                                                      'app_folder')

                dbox_session.set_token(secret, token)
                self.dbox_client = client.DropboxClient(dbox_session)

            except Exception, e:
                log.warn(e)



    def upload(self, src, dst):

        log.debug('source: %s' % src)
        log.debug('dst: %s' % dst)

        if USE_CELERYD:
            self.upload_task.delay(self, src, dst)
            #dbox_upload.delay(self, src, dst)
        else:
            self.upload_task(self, src, dst)
            #dbox_upload(self, src, dst)

    @task
    def upload_task(obj, src, dst):

        if obj.dbox_client:
            try:
                f = open(src)
                response = obj.dbox_client.put_file(dst, f)
                print "uploaded:", response
            except Exception, e:
                log.warn(e)


