import pytest
import requests

from test_data import users
from settings import urls


USERS = [users.user1, users.user2, users.user3, users.user4]


class TestUserGETMethod(object):
    @pytest.fixture()
    def setup(self):
        # Checking site availability
        try:
            requests.get(urls.BASE_URL)
        except requests.ConnectionError:
            raise AssertionError("Connection Error Ocurred")
        else:
            return requests.get(urls.USERS_URL)

    def teardown(self):
        pass

    def test_user_id(self):
        for user in USERS:
            r = requests.get("{}/{}".format(urls.USERS_URL, user['id']))
            assert r.json()['id'] == user['id']

    def test_user_name(self):
        for user in USERS:
            r = requests.get("{}/{}".format(urls.USERS_URL, user['id']))
            assert r.json()['name'] == user['name']

    def test_user_email(self):
        for user in USERS:
            r = requests.get("{}/{}".format(urls.USERS_URL, user['id']))
            assert r.json()['email'] == user['email']

    def test_user_address(self):
        for user in USERS:
            r = requests.get("{}/{}".format(urls.USERS_URL, user['id']))
            assert r.json()['address']['street'] == user['address']['street']
            assert r.json()['address']['suite'] == user['address']['suite']
            assert r.json()['address']['city'] == user['address']['city']
            assert r.json()['address']['zipcode'] == user['address']['zipcode']
            assert r.json()['address']['geo'] == user['address']['geo']

    def test_user_website(self):
        for user in USERS:
            r = requests.get("{}/{}".format(urls.USERS_URL, user['id']))
            assert r.json()['website'] == user['website']

    def test_user_company(self):
        for user in USERS:
            r = requests.get("{}/{}".format(urls.USERS_URL, user['id']))
            assert r.json()[
                'company']['catchPhrase'] == user['company']['catchPhrase']
            assert r.json()['company']['name'] == user['company']['name']
            assert r.json()['company']['bs'] == user['company']['bs']

    def test_user_quantity(self, setup):
        assert len(setup.json()) == users.USER_QUANTITY
