API_BASE = 'https://api.gotinder.com'

USER_AGENT = 'Tinder/4.6.1 (iPhone; iOS 9.0.1; Scale/2.00)'

HEADERS = {
    "User-Agent": USER_AGENT,
    "os_version": "90000000001",
    "app-version": "371",
    "platform": "android",  # XXX with ios we run in an error
    "Content-type": "application/json; charset=utf-8"
}

GENDER_MAP = ["male", "female"]

GENDER_MAP_REVERSE = {"male": 0, "female": 1}

UPDATABLE_FIELDS = [
    'gender', 'age_filter_min', 'age_filter_max',
    'distance_filter', 'age_filter_min', 'bio', 'interested_in'
]
