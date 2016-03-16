from time import time

from . import api
from . import models


class Session(object):

    def __init__(self, facebook_id, facebook_token, XAuthToken=None, proxies=None):
        self._api = api.TinderAPI(XAuthToken, proxies)
        # perform authentication
        if XAuthToken is None:
            self._api.auth(facebook_id, facebook_token)
        self.profile = models.Profile(self._api.profile(), self._api)

    def nearby_users(self, limit=10):
        response = self._api.recs(limit)
        users = response['results'] if 'results' in response else []
        ret = []
        for u in users:
            if not u["_id"].startswith("tinder_rate_limited_id_"):
                ret.append(models.Hopeful(u, self))
        return ret

    def update_profile(self, profile):
        return self._api.update_profile(profile)

    def update_location(self, latitude, longitude):
        return self._api.ping(latitude, longitude)

    def matches(self):
        return [models.Match(m, self) for m in self._api.matches()]

    @property
    def likes_remaining(self):
        meta_dct = self._api.meta()
        return meta_dct['rating']['likes_remaining']

    @property
    def can_like_in(self):
        '''
        Return the number of seconds before being allowed to issue likes
        '''
        meta_dct = self._api.meta()
        now = int(time())
        limited_until = meta_dct['rating'].get(
            'rate_limited_until', now)  # Milliseconds
        return limited_until / 1000 - now

    @property
    def banned(self):
        return self.profile.banned
