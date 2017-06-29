# -*- coding: utf-8 -*-

import os
import logging
import requests
from django.core.checks import register, Tags, Error, Warning, Info, Debug, Critical
from django.conf import settings

log = logging.getLogger(__name__)

@register()
def check_binaries(app_configs, **kwargs):
    """
    checks existance of configured binaries
    """

    BINARIES_TO_CHECK = [
        'LAME_BINARY',
        'SOX_BINARY',
        'FAAD_BINARY',
        'FFPROBE_BINARY',
        'ECHOPRINT_CODEGEN_BINARY',
    ]

    errors = []

    for key in BINARIES_TO_CHECK:
        path = getattr(settings, key, None)
        if not path:

            errors.append(
                Error(
                    'binary missing',
                    hint='binary location {} not specified in settings'.format(key),
                    obj=key,
                    id='platform_base.E001',
                )
            )

        elif not os.path.isfile(path):

            errors.append(
                Error(
                    'path does not exist',
                    hint='binary location for {} does not exist at {}'.format(key, path),
                    obj=key,
                    id='platform_base.E001',
                )
            )

        else:

            errors.append(
                Debug(
                    'OK: {}'.format(path),
                    #hint='{} found: {}'.format(key, path),
                    obj=key,
                    id='platform_base.I001',
                )
            )


    return errors


@register()
def check_directories(app_configs, **kwargs):
    """
    check platform directories
    """

    PATHS_TO_CHECK = [
        'MEDIA_ROOT',
    ]

    errors = []

    for key in PATHS_TO_CHECK:
        path = getattr(settings, key, None)

        if not os.path.isdir(path):

            errors.append(
                Error(
                    'path does not exist',
                    hint='location for {} does not exist at {}'.format(key, path),
                    obj=key,
                    id='platform_base.E002',
                )
            )

        else:

            errors.append(
                Debug(
                    'OK: {}'.format(path),
                    #hint='{} found: {}'.format(key, path),
                    obj=key,
                    id='platform_base.I002',
                )
            )


    return errors


@register()
def check_apis(app_configs, **kwargs):
    """
    check API connection
    """

    SERVICES_TO_CHECK = [
        {
            'name': 'Musicbrainz API',
            'url': 'http://{}/ws/2/artist/1582a5b8-538e-45e7-9ae4-4099439a0e79'.format(getattr(settings, 'MUSICBRAINZ_HOST')),
        },
        {
            'name': 'Discogs API',
            'url': 'http://{}/labels/1'.format(getattr(settings, 'DISCOGS_HOST'))
        }
    ]

    errors = []

    for service in SERVICES_TO_CHECK:

        r = requests.get(service['url'])

        if not r.status_code == 200:

            errors.append(
                Error(
                    'connection error ({})'.format(r.status_code),
                    hint='unable to connect to: {}'.format(service['url']),
                    obj=service['name'],
                    id='platform_base.E003',
                )
            )

        else:

            errors.append(
                Debug(
                    'OK: {}'.format(service['url']),
                    obj=service['name'],
                    id='platform_base.I003',
                )
            )


    return errors
