import pynder

FBTOKEN = "YOUR_FB_TOKEN"
FBID = "YOUR_FB_ID"

session = pynder.Session(FBID, FBTOKEN)
users = session.nearby_users()
for user in users[:5]:
    print user.like()
