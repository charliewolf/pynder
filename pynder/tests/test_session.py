import os
import vcr
import unittest
import pynder

from pynder.tests.utils import read_test_ini, FILE_DIR


my_vcr = vcr.VCR(
    cassette_library_dir=os.path.join(FILE_DIR, "vcr/session"),
    record_mode="new_episodes",
)


class TestSession(unittest.TestCase):

    def setUp(self):
        pass

    @my_vcr.use_cassette(filter_post_data_parameters=["facebook_id",
                                                      "facebook_token"])
    def test_login(self):
        auth = read_test_ini()
        session = pynder.Session(auth["facebook_id"], auth["facebook_token"])
        self.assertEqual(session.profile.gender, "male")

    @my_vcr.use_cassette(filter_post_data_parameters=["facebook_id",
                                                      "facebook_token"])
    def test_nearby_users_empty(self):
        auth = read_test_ini()
        session = pynder.Session(auth["facebook_id"], auth["facebook_token"])
        self.assertEqual(session.nearby_users(limit=10), [])
