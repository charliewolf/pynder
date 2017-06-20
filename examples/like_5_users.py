import itertools
import pynder

FBTOKEN = "YOUR_FB_TOKEN"
FBID = "YOUR_FB_ID"

session = pynder.Session(facebook_id=FBID, facebook_token=FBTOKEN)
users = session.nearby_users()
for user in itertools.islice(users, 5):
    print user.like()
