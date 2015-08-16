from . import api
from . import models


class Session(object):

    def __init__(self, facebook_id, facebook_token):
        self._api = api.TinderAPI()
        # perform authentication
        self._api.auth(facebook_id, facebook_token)
        self.profile = models.Profile(self._api.profile(), self)

    def nearby_users(self):
        return [models.Hopeful(u, self) for u in self._api.recs()['results']]

    def update_location(self, latitude, longitude):
        return self._api.ping(latitude, longitude)

    def matches(self):
        return [models.Match(m, self) for m in self._api.matches()]
