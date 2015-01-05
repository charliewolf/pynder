import dateutil.parser


class Message(object):

    def __init__(self, data, user=None):
        if isinstance(data, str):
            self.body = data
        else:
            self._data = data
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
                self.sent = dateutil.parser.parse(data['sent_date'])

    def __repr__(self):
        return self.body

    def __str__(self):
        return self.body
