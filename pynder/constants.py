API_BASE = 'https://api.gotinder.com'

USER_AGENT = 'Tinder Android Version 4.1.3'

HEADERS = {"User-Agent": USER_AGENT, "os_version": "19", "app-version": "759", "platform": "android", "Content-type": "application/json; charset=utf-8"}

GENDER_MAP = ["male", "female"]

GENDER_MAP_REVERSE = {"male":0,"female":1}

UPDATABLE_FIELDS = ['gender', 'age_filter_min', 'age_filter_max', 'distance_filter', 'age_filter_min', 'bio', 'interested_in']
