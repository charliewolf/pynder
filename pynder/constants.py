API_BASE = "https://api.gotinder.com"

USER_AGENT = "Tinder/6.8.0 (iPhone; iOS 9.0.2; Scale/2.00)"

HEADERS = {
	"x-client-version":	"68023",
	"app-version": "1824",
	"Accept-Encoding": "gzip, deflate",
	"platform": "ios",
	"Accept-Language": "it;q=1, en-US;q=0.9",
	"Accept": "*/*",
	"Connection": "keep-alive",
	"os_version": "90000000002",
	"Content-type": "application/json; charset=utf-8"
}

GENDER_MAP = ["male", "female"]

GENDER_MAP_REVERSE = {"male": 0, "female": 1}

UPDATABLE_FIELDS = [
    'gender', 'age_filter_min', 'age_filter_max',
    'distance_filter', 'age_filter_min', 'bio', 'interested_in'
]
