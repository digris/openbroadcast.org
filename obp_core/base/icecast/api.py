import requests
import logging

log = logging.getLogger(__name__)


class IcecastAPIClient:
    def __init__(self, server, mountpoint, admin_user, admin_pass):

        self.server = server
        self.mountpoint = mountpoint
        self.admin_user = admin_user
        self.admin_pass = admin_pass

    def set_text(self, text):

        if self.server and self.admin_user and self.admin_pass:
            url = "%sadmin/metadata" % self.server
            auth = (self.admin_user, self.admin_pass)
            params = {
                "mount": "/%s" % self.mountpoint,
                "mode": "updinfo",
                "song": "%s" % text,
            }
            r = requests.get(url, auth=auth, params=params, timeout=2.0)

            if r.status_code != 200:
                log.warning(f"API: {r.url} - status: {r.status_code}")
            else:
                log.debug(f"API: {r.url} - status: {r.status_code}")


def set_stream_metadata(channel, text):
    log.info(f"channel: {channel} - metadata-text: {text}")
    try:
        api = IcecastAPIClient(
            server=channel.icecast2_server,
            mountpoint=channel.icecast2_mountpoint,
            admin_user=channel.icecast2_admin_user,
            admin_pass=channel.icecast2_admin_pass,
        )
        api.set_text(text)
    except Exception as e:
        log.warning("unable to set stream metadata text: %s" % e)
