import dateutil.parser
from datetime import date
from .. import constants
from .message import Message


class User(object):
    def __init__(self, data, session):
        self._session = session
        self._data = data
        self.id = data['_id']

        SIMPLE_FIELDS = "name bio gender birth_date common_interests common_connections ping_time".split(" ")
        for f in SIMPLE_FIELDS:
            setattr(self, f, data[f])

        self.gender = constants.GENDER_MAP[int(data['gender'])]
        self.photos_obj = [p for p in data['photos']]
        self.birth_date = dateutil.parser.parse(self.birth_date)
        self.common_interests = [p['name'] for p in data['common_interests']]
        self.common_connections = [p['name'] for p in data['common_connections']]

    @property
    def thumbnails(self):
        return self.get_photos(width="84")

    @property
    def photos(self):
        return self.get_photos()

    @property
    def distance_km(self):
        if self._data.get("distance_mi", False) or self._data.get("distance_km",False):
            return self._data.get('distance_km', self._data['distance_mi'] * 1.60934)
        else:
            return 0

    @property
    def age(self):
        today = date.today()
        return (today.year - self.birth_date.year -
                    ((today.month, today.day) <
                     (self.birth_date.month, self.birth_date.day)))

    def __unicode__(self):
        return u"{n} ({a})".format(n=self.name, a=self.age)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return repr(self.name)

    def report(self, cause):
        return self._session._api.report(self.id, cause)

    def get_photos(self, width=None):
        photos_list = []
        for photo in self.photos_obj:
            if width is None:
                photos_list.append(photo.get("url"))
            else:
                sizes = ["84","172","320","640"]
                if width not in sizes:
                    print "Only support these widths: %s" %sizes
                    return None
                for p in photo.get("processedFiles", []):
                    if p.get("width", 0) == int(width):
                        photos_list.append(p.get("url", None))
        return photos_list
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

    def message(self, body):
        return self._session._api.message(self.id, body)['_id']

    def delete(self):
        return self._session._api._request('DELETE', '/user/matches/' + self.id)

    def __repr__(self):
        return "<Unnamed match>" if self.user is None else repr(self.user)
