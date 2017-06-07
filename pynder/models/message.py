import dateutil.parser
from six import text_type
from pynder.models.base import Model


class Message(Model):

    def __init__(self, data, user=None):
        self._data = data
        self.id = data['_id']
        self.sent = dateutil.parser.parse(data['sent_date'])
        self.body = data['message']
        if user:
            if data['from'] == user.id:
                self.sender = user
            if data['to'] == user.id:
                self.to = user
            if data['from'] == user._session.profile.id:
                self.sender = user._session.profile
            if data['to'] == user._session.profile.id:
                self.to = user._session.profile
            self._session = user._session

    def like(self):
        return self._session._api.like_message(self)

    def unlike(self):
        return self._session._api.unlike_message(self)

    @property
    def is_liked(self, since=None):
        for liked_message in self._session._api.liked_messages(since):
            if self.id == liked_message['message_id']:
                return liked_message['is_liked']
        return False

    def __unicode__(self):
        return self.body

    def __str__(self):
        return text_type(self).encode("utf8")

    def __repr__(self):
        return repr(self.body)
