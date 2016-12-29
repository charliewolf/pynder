API_BASE = 'https://api.gotinder.com'

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

GENDER_MAP = ["male", "female"]

GENDER_MAP_REVERSE = {"male": 0, "female": 1}

UPDATABLE_FIELDS = [
    'gender', 'age_filter_min', 'age_filter_max',
    'distance_filter', 'age_filter_min', 'bio', 'interested_in'
]

SIMPLE_FIELDS = ("name", "bio", "birth_date", "ping_time")
