from enum import Enum

API_BASE = 'https://api.gotinder.com'
CONTENT_BASE = 'https://content.gotinder.com'

USER_AGENT = 'Tinder Android Version 6.4.1'

HEADERS = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": USER_AGENT,
    "Host": API_BASE,
    "os_version": "1935",
    "app-version": "371",
    "platform": "android",  # XXX with ios we run in an error
    "Accept-Encoding": "gzip"
}

GENDER_MAP = ("male", "female")

GENDER_MAP_REVERSE = {"male": 0, "female": 1}

UPDATABLE_FIELDS = [
    'gender', 'age_filter_min', 'age_filter_max',
    'distance_filter', 'bio', 'interested_in',
    'discoverable'
]

SIMPLE_FIELDS = {"name", "bio", "birth_date", "ping_time"}

VALID_PHOTO_SIZES = {84, 172, 320, 640}


class ReportCause(Enum):
    Other = 0
    Spam = 1
    Inappropriate_Photos = 4
    Bad_Offline_Behavior = 5
    Inappropriate_Messages = 6
