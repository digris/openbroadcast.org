import logging

logger = logging.getLogger(__name__)


def reassign_media(release, media_qs):
    logger.debug(f"re-assign media {media_qs} to {release}")

    for media in media_qs:
        media.release = release
        media.save()

    release.refresh_from_db()

    return release
