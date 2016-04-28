# -*- coding: utf-8 -*-
import logging
from social_auth.backends.contrib.dropbox import DropboxBackend
from social_auth.models import UserSocialAuth
from dropbox import client, session
from django.conf import settings

DROPBOX_APP_ID = getattr(settings, 'DROPBOX_APP_ID')
DROPBOX_API_SECRET = getattr(settings, 'DROPBOX_API_SECRET')

def post_connect_tasks(backend, details, response, user=None, is_new=False, *args, **kwargs):

    if user is None:
        return

    if isinstance(backend, DropboxBackend):
        try:
            dropbox_post_connect_tasks(backend, details, response, user, is_new, *args, **kwargs)
        except Exception as e:
            pass


def dropbox_post_connect_tasks(backend, details, response, user=None, is_new=False, *args, **kwargs):

    from dropbox import Dropbox, DropboxTeam, create_session

    print 'dropbox_post_connect_tasks'

    print 'backend:  %s' % backend
    print 'details:  %s' % details
    print 'response: %s' % response
    print 'user:     %s' % user
    print 'is_new:   %s' % is_new
    print

    # Get Access Token and Secret
    try:
        social_user = UserSocialAuth.objects.get(user=user, provider='dropbox')
    except UserSocialAuth.DoesNotExist:
        social_user = None

    print social_user

    access_token = social_user.tokens['access_token']


    token = access_token.split('&')[0].split('=')[1]
    secret = access_token.split('&')[1].split('=')[1]

    print 'token:  %s' % token
    print 'secret: %s' % secret

    sess = session.DropboxSession(DROPBOX_APP_ID, DROPBOX_API_SECRET)
    sess.set_token(token, secret)
    c = client.DropboxClient(sess)

    oauth2_access_token = c.create_oauth2_access_token()

    print oauth2_access_token

    dbx = Dropbox(oauth2_access_token)



    paths = [
        '/Downloads',
        '/Uploads',
        '/Uploads [completed]',
        '/Uploads [errors]',
    ]

    for path in paths:
        try:
            dbx.files_create_folder(path)
        except Exception as e:
            print e


    # dbox_session = session.DropboxSession(DROPBOX_APP_ID, DROPBOX_API_SECRET, 'app_folder')
    #
    # dbox_session.set_token(secret, token)
    # dbox_client = client.DropboxClient(dbox_session)
    #
    # dbox_client.file_create_folder('just-a-test')