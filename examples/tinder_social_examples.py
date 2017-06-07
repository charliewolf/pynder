import pynder

FBID = "YOUR_FB_ID"
FBTOKEN= "YOUR_FB_TOKEN"

session = pynder.Session(facebook_id=FBID, facebook_token=FBTOKEN)
friends = session.get_fb_friends()

# Print the names of all facebook friends using Tinder Social.
print(", ".join([x.name for x in friends]))

# Get the user_info of these facebook friends.
user_info_objects = []
for friend in friends:
    user_info_objects.append(friend.get_tinder_information())

# Print the bios.
for user_info, friend in zip(user_info_objects, friends):
    print("=" * 50)
    # Use Friend.name, as user_info.name only contains first name.
    print(friend.name)
    print(friend.facebook_link)
    print("-" * 50)
    print(user_info.bio)
    print("=" * 50)
