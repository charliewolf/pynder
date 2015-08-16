import dateutil.parser
from datetime import date
from .. import constants
from .message import Message


class User(object):
    def __init__(self, data, session):
        self._session = session
        self._data = data
        self.id = data['_id']

        SIMPLE_FIELDS = "name bio birth_date common_friends common_likes ping_time".split(" ")
        for f in SIMPLE_FIELDS:
            setattr(self, f, data[f])

        self.gender = constants.GENDER_MAP[int(data['gender'])]
        self.photos = [p['url'] for p in data['photos']]
        self.birth_date = dateutil.parser.parse(self.birth_date)

    @property
    def distance_km(self):
        assert "distance_mi" in self._data or "distance_km" in self._data
        return self._data.get('distance_km', self._data['distance_mi'] * 1.60934)

    @property
    def age(self):
        today = date.today()
        return (today.year - self.birth_date.year -
                    ((today.month, today.day) <
                     (self.birth_date.month, self.birth_date.day)))

    def __repr__(self):
        return self.name

    def report(self, cause):
        return self._session._api.report(self.id, cause)


class Hopeful(User):
    def like(self):
        return self._session._api.like(self.id)['match']

    def dislike(self):
        return self._session._api.dislike(self.id)


class Match(object):
    def __init__(self, match, _session):
        self._session = _session
        self.id = match["_id"]
        self.user, self.messages = None, []
        if 'person' in match:
            user_data = _session._api.user_info(match['person']['_id'])['results']
            user_data['_id'] = match['person']['_id']
            self.user = User(user_data, _session)
            self.messages = [Message(m, user=self.user) for m in match['messages']]

    @property
    def name(self):
        return "Unnamed match" if self.user is None else self.user.name

    def message(self, body):
        return self._session._api.message(self.id, body)['_id']
