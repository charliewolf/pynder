import requests
import json
import threading
from . import constants
from . import errors


class TinderAPI(object):

    def __init__(self, XAuthToken=None, proxies=None):
        self._session = requests.Session()
        self._session.headers.update(constants.HEADERS)
        self._token = XAuthToken
        self._proxies = proxies
        if XAuthToken is not None:
            self._session.headers.update({"X-Auth-Token": str(XAuthToken)})

    def _url(self, path):
        return constants.API_BASE + path

    def auth(self, facebook_id, facebook_token):
        data = json.dumps({"facebook_id": str(facebook_id),
                           "facebook_token": facebook_token})
        result = self._session.post(
            self._url('/auth'), data=data, proxies=self._proxies).json()
        if 'token' not in result:
            raise errors.RequestError("Couldn't authenticate")
        self._token = result['token']
        self._session.headers.update({"X-Auth-Token": str(result['token'])})
        return result

    def _request(self, method, url, data={}):
        if not hasattr(self, '_token'):
            raise errors.InitializationError
        result = self._session.request(method, self._url(
            url), data=json.dumps(data), proxies=self._proxies)
        while result.status_code == 429:
            blocker = threading.Event()
            blocker.wait(0.01)
            result = self._session.request(method, self._url(
                url), data=data, proxies=self._proxies)
        if result.status_code != 200:
            raise errors.RequestError(result.status_code)
        return result.json()

    def _get(self, url):
        return self._request("get", url)

    def _post(self, url, data={}):
        return self._request("post", url, data=data)

    def updates(self):
        return self._post("/updates")

    def meta(self):
        return self._get("/meta")

    def recs(self, limit=10):
        return self._post("/user/recs", data={"limit": limit})

    def matches(self):
        return self.updates()['matches']

    def profile(self):
        return self._get("/profile")

    def update_profile(self, profile):
        return self._post("/profile", profile)

    def like(self, user):
        return self._get("/like/{}".format(user))

    def dislike(self, user):
        return self._get("/pass/{}".format(user))

    def message(self, user, body):
        return self._post("/user/matches/{}".format(user),
                          {"message": str(body)})

    def report(self, user, cause=1):
        return self._post("/report/" + user, {"cause": cause})

    def user_info(self, user_id):
        return self._get("/user/" + user_id)

    def ping(self, lat, lon):
        return self._post("/user/ping", {"lat": lat, "lon": lon})

    def superlike(self, user):
        result = self._post("/like/{}/super".format(user))
        if 'limit_exceeded' in result and result['limit_exceeded']:
            raise errors.RequestError("Superlike limit exceeded")
        return result
