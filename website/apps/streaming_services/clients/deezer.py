# -*- coding: utf-8 -*-
import requests

BASE_URL = "https://api.deezer.com"


class DeezerAPIClient(object):
    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token
        self.base_url = BASE_URL

    def _search_media(self, media):

        url = "{base_url}/search".format(base_url=self.base_url)

        q = u'track:"{track}" artist:"{artist}" album:"{album}"'.format(
            track=media.name, artist=media.artist.name, album=media.release.name,
        )

        params = {
            "order": "RANKING",
            "access_token": self.access_token,
            "q": q,
        }

        r = requests.get(url, params)
        results = r.json().get("data", [])

        if results:
            return results[0].get("id")

        return None

    def _add_media_to_favorites(self, deezer_id):

        url = "{base_url}/user/{user_id}/tracks".format(
            base_url=self.base_url, user_id=self.user_id
        )

        params = {
            "access_token": self.access_token,
        }

        payload = {"track_id": deezer_id}

        requests.post(url, data=payload, params=params)

    def _remove_media_from_favorites(self, deezer_id):

        url = "{base_url}/user/{user_id}/tracks".format(
            base_url=self.base_url, user_id=self.user_id
        )

        params = {"access_token": self.access_token, "track_id": deezer_id}

        requests.delete(url, params=params)

    def add_to_favorites(self, obj):

        if obj.__class__.__name__ == "Media":
            deezer_id = self._search_media(obj)
            if deezer_id:
                self._add_media_to_favorites(deezer_id=deezer_id)

    def remove_from_favorites(self, obj):

        if obj.__class__.__name__ == "Media":
            deezer_id = self._search_media(obj)
            if deezer_id:
                self._remove_media_from_favorites(deezer_id=deezer_id)
