import dateutil.parser


class Message(object):

    def __init__(self, data, user=None):
        self._data = data
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

    def __repr__(self):
        return self.body

    def __str__(self):
        return self.body
