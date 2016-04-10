import dateutil.parser
from datetime import date
from .. import constants
from six import text_type
from .message import Message


class User(object):

    def __init__(self, data, session):
        self._session = session
        self._data = data
        self.id = data['_id']

        SIMPLE_FIELDS = ("name", "bio", "birth_date", "ping_time")
        for f in SIMPLE_FIELDS:
            setattr(self, f, data[f])

        self.photos_obj = [p for p in data['photos']]
        self.birth_date = dateutil.parser.parse(self.birth_date)
        self.schools = []
        self.jobs = []
        try:
            self.schools.extend([school["name"] for school in data['schools']])
            self.jobs.extend(["%s @ %s" % (job["title"]["name"], job["company"][
                             "name"]) for job in data['jobs'] if 'title' in job and 'company' in job])
            self.jobs.extend(["%s" % (job["company"]["name"],) for job in data[
                             'jobs'] if 'title' not in job and 'company' in job])
            self.jobs.extend(["%s" % (job["title"]["name"],) for job in data[
                             'jobs'] if 'title' in job and 'company' not in job])
        except ValueError:
            pass

    @property
    def instagram_username(self):
        if self._data.get("instagram", False):
            return self._data['instagram']['username']

    @property
    def instagram_photos(self):
        if self._data.get("instagram", False):
            return [p for p in self._data['instagram']['photos']]

    @property
    def gender(self):
        return constants.GENDER_MAP[int(self._data['gender'])]

    @property
    def common_interests(self):
        return [p for p in self._data['common_interests']]

    @property
    def common_connections(self):
        return [p for p in self._data['common_friends']]

    @property
    def thumbnails(self):
        return self.get_photos(width="84")

    @property
    def photos(self):
        return self.get_photos()

    @property
    def distance_km(self):
        if self._data.get("distance_mi", False) or self._data.get("distance_km", False):
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
        return text_type(self).encode('utf-8')

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
                sizes = ["84", "172", "320", "640"]
                if width not in sizes:
                    print("Only support these widths: %s" % sizes)
                    return None
                for p in photo.get("processedFiles", []):
                    if p.get("width", 0) == int(width):
                        photos_list.append(p.get("url", None))
        return photos_list


class Hopeful(User):

    def like(self):
        return self._session._api.like(self.id)['match']

    def superlike(self):
        return self._session._api.superlike(self.id)['match']

    def dislike(self):
        return self._session._api.dislike(self.id)


class Match(object):

    def __init__(self, match, _session):
        self._session = _session
        self.id = match["_id"]
        self.user, self.messages = None, []
        if 'person' in match:
            user_data = _session._api.user_info(
                match['person']['_id'])['results']
            user_data['_id'] = match['person']['_id']
            self.user = User(user_data, _session)
            self.messages = [Message(m, user=self.user)
                             for m in match['messages']]

    def message(self, body):
        return self._session._api.message(self.id, body)['_id']

    def delete(self):
        return self._session._api._request('DELETE', '/user/matches/' + self.id)

    def __repr__(self):
        return "<Unnamed match>" if self.user is None else repr(self.user)
