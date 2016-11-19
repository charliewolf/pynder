import pynder

"""
Like the last message sent by all your matches
"""

session = pynder.Session(XAuthToken="YOUR_AUTH_TOKEN")
me = session.profile
for u in session.matches():
    for m in reversed(u.messages):
        if m.to.id == me.id:
            m.like()
            break
