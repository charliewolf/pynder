pynder
=======

This is a python client for the `Tinder <http://gotinder.com>`_ API.

Please see the examples for more information on how to use.

You start by instantiating a pynder.Session object with a Facebook ID and Facebook access token.

Once your session is initialized you have the following methods / attributes: ::


  pynder.nearby_users() # returns a list of users nearby
  pynder.matches() # get users you have already been matched with
  pynder.update_location(LAT, LON) # updates latitude and longitude for your profile
  pynder.profile  # your profile. If you update its attributes they will be updated on Tinder.

When you run nearby_users you will receive a list of `Hopeful` objects. 
These have the following properties: ::

  user.bio # their biography
  user.name # their name
  user.photo # a list of photo URLs
  user.thumbnail #a list of thumbnails of photo URLS
  user.age # their age
  user.birth_date # their birth_date
  user.ping_time # last online
  user.distance_km # distane from you
  user.common_connections # friends in common
  user.common_interests # likes in common - returns a list of {'name':NAME, 'id':ID}
  user.get_photos(width=WIDTH) # a list of photo URLS with either of these widths ["84","172","320","640"]
	user.instagram_username # instagram username
	user.instagram_photos # a list of instagram photos with these fields for each photo: 'image','link','thumbnail'

You may run `user.like()`, `user.superlike()` or `user.dislike()` on that user.

For your list of matches, they will have the same attributes as above except you can't dislike or like them. You can, however, see any messages exchanged (`match.messages`)   or send them a message yourself (`match.message("Eyyyy gurl")`).

Please let me know if you have any questions or bug reports.
