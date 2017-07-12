import requests
import threading
import pynder.constants as constants
import pynder.errors as errors


class TinderAPI(object):

    def __init__(self, XAuthToken=None, proxies=None):
        self._session = requests.Session()
        self._session.headers.update(constants.HEADERS)
        self._token = XAuthToken
        self._proxies = proxies
        if XAuthToken is not None:
            self._session.headers.update({"X-Auth-Token": str(XAuthToken)})

    def _full_url(self, url):
        _url = url.lower()

        if _url.startswith("http://") or _url.startswith("https://"):
            return url
        else:
            return constants.API_BASE + url

    def auth(self, facebook_id, facebook_token):
        data = {"facebook_id": str(facebook_id), "facebook_token": facebook_token}
        result = self._session.post(
            self._full_url('/auth'), json=data, proxies=self._proxies).json()
        if 'token' not in result:
            raise errors.RequestError("Couldn't authenticate")
        self._token = result['token']
        self._session.headers.update({"X-Auth-Token": str(result['token'])})
        return result

    def _request(self, method, url, data={}):
        if not hasattr(self, '_token'):
            raise errors.InitializationError
        result = self._session.request(method, self._full_url(
            url), json=data, proxies=self._proxies)
        while result.status_code == 429:
            blocker = threading.Event()
            blocker.wait(0.01)
            result = self._session.request(method, self._full_url(
                url), data=data, proxies=self._proxies)
        if result.status_code < 200 or result.status_code >= 300:
            raise errors.RequestError(result.status_code)
        if result.status_code == 201 or result.status_code == 204:
            return {}
        return result.json()

    def _get(self, url):
        return self._request("get", url)

    def _post(self, url, data={}):
        return self._request("post", url, data=data)

    def _delete(self, url):
        return self._request("delete", url)

    def updates(self, since):
        return self._post("/updates", {"last_activity_date": since} if since else {})

    def meta(self):
        return self._get("/meta")

    def add_profile_photo(self, fbid, x_dist, y_dist, x_offset, y_offset):
        data = {
                "transmit": "fb",
                "assets": [{"id": str(fbid), "xdistance_percent": float(x_dist), "ydistance_percent": float(y_dist),
                            "xoffset_percent": float(x_offset), "yoffset_percent": float(y_offset)}]
               }

        return self._request("post", constants.CONTENT_BASE + "/media", data=data)

    def delete_profile_photo(self, photo_id):
        data = {"assets": [photo_id]}

        return self._request("delete", constants.CONTENT_BASE + "/media", data=data)

    def recs(self, limit=10):
        return self._post("/user/recs", data={"limit": limit})

    def matches(self, since):
        return self.updates(since)['matches']

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

    def message_gif(self, user, giphy_id):
        return self._post("/user/matches/{}".format(user),
                          {"type": "gif", "gif_id": str(giphy_id)})

    def report(self, user, cause=constants.ReportCause.Other, text=""):
        try:
            cause = int(cause)
        except TypeError:
            cause = int(cause.value)

        data = {"cause": cause}

        if text and constants.ReportCause(cause) == constants.ReportCause.Other:
            data["text"] = text

        return self._post("/report/" + user, data)

    def user_info(self, user_id):
        return self._get("/user/" + user_id)

    def ping(self, lat, lon):
        return self._post("/user/ping", {"lat": lat, "lon": lon})

    def share(self, user):
        return self._post("/user/{}/share".format(user))

    def superlike(self, user):
        result = self._post("/like/{}/super".format(user))
        if 'limit_exceeded' in result and result['limit_exceeded']:
            raise errors.RequestError("Superlike limit exceeded")
        return result

    def fb_friends(self):
        """
        Requests records of all facebook friends using Tinder Social.
        :return: object containing array of all friends who use Tinder Social.
        """
        return self._get("/group/friends")

    def like_message(self, message):
        """
        Hearts a message sent by a match
        :param message: message id
        :return: empty json, response code is 201 (Created)
        """
        return self._post("/message/{}/like".format(message.id))

    def unlike_message(self, message):
        """
        Removes heart from a message
        :param message: message id
        :return: empty json, response code is 204 (No content)
        """
        return self._delete("/message/{}/like".format(message.id))

    def liked_messages(self, since):
        return self.updates(since)['liked_messages']
