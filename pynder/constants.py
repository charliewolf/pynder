from enum import Enum

API_BASE = 'https://api.gotinder.com'
CONTENT_BASE = 'https://content.gotinder.com'

USER_AGENT = "Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)"

HEADERS = {
    'app_version': '6.9.4',
    'platform': 'ios',
    "content-type": "application/json",
    "User-agent": USER_AGENT,
    "Accept": "application/json"
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
