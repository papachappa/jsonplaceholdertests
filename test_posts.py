import re

import requests
import pytest

from settings import urls
from test_data import (users,  posts)

USERS = [users.user1, users.user2, users.user3, users.user4]


class TestPostsGETMethod(object):
    @pytest.fixture()
    def setup(self):
        # Checking site availability
        try:
            requests.get(urls.BASE_URL)
        except requests.ConnectionError:
            raise AssertionError("Connection Error Ocurred")
        else:
            return requests.get(urls.POSTS_URL)

    def teardown(self):
        pass

    def test_posts_quantity(self, setup):
        assert len(setup.json()) == posts.POSTS_OVERALL_QUANTITY

    @pytest.fixture()
    def test_posts_user1_quantity(self):
        r = requests.get(urls.POSTS_URL, params=posts.user1_qty_payload_get)
        assert len(r.json()) == posts.POSTS_USER1_QUANTITY
        return r

    def test_all_title_comments_from_user1(self, test_posts_user1_quantity):
        list_to_check = [r['title'] for r in test_posts_user1_quantity.json()]
        res = list(set(list_to_check) - set(posts.user1_comments))
        assert res == []

    def trim_string(self, string):
        return re.sub(r'\s+', '', string)

    def test_posts_id86_title_body(self):
        r = requests.get(urls.POSTS_URL, params=posts.id86_title_body_payload_get)
        assert r.json()[0]['title'] == posts.POSTS_ID_86_TITLE
        assert self.trim_string(
            r.json()[0]['body']) == self.trim_string(posts.POSTS_ID_86_BODY)


class TestUserPostsPOSTMethod(object):
    def setup(self):
        # Checking site availability
        try:
            requests.get(urls.BASE_URL)
        except requests.ConnectionError:
            raise AssertionError("Connection Error Ocurred")

    def teardown(self):
        pass

    def test_posts_user1_title_created(self):
        r = requests.post(
            urls.POSTS_URL, data=posts.user1_title_payload_post
        )
        assert r.status_code == 201
        assert r.json()['userid'] == '1'
        assert r.json()['id'] == '103'
        assert r.json()['title'] == 'test'

    def test_posts_user1_year_created(self):
        r = requests.post(
            urls.POSTS_URL, data=posts.user1_year_payload_post
        )
        assert r.status_code == 201
        assert r.json()['userid'] == '1'
        assert r.json()['year'] == '2001'


class TestUserPostsPUTMethod(object):
    def setup(self):
        # Checking site availability
        try:
            requests.get(urls.BASE_URL)
        except requests.ConnectionError:
            raise AssertionError("Connection Error Ocurred")

    def teardown(self):
        pass

    def test_posts_users_title_year(self):
        for user in USERS:
            r = requests.put(
                "{}/{}".format(urls.POSTS_URL, user['id']),
                data=posts.users_title_year_payload_post
            )
            assert r.status_code == 200

    def test_negative_posts_title_year(self):
        r = requests.put(
            "{}/{}".format(urls.POSTS_URL, posts.not_existed_user_post),
            data=posts.users_title_year_payload_post
        )
        assert r.status_code == 404


class TestUserPostsPATCHMethod(object):
    def setup(self):
        # Checking site availability
        try:
            requests.get(urls.BASE_URL)
        except requests.ConnectionError:
            raise AssertionError("Connection Error Ocurred")

    def teardown(self):
        pass

    def test_posts_users_title_year(self):
        for user in USERS:
            r = requests.patch(
                "{}/{}".format(urls.POSTS_URL, user['id']),
                data=posts.users_title_year_payload_post
            )
            assert r.status_code == 200
            assert r.json()['title'] == 'Book1'
            assert r.json()['year'] == '2010'

    def test_empty_message_body(self):
        r = requests.patch(
            "{}/{}".format(urls.POSTS_URL, '1000')
        )
        assert r.status_code == 404

    def test_header_server_type(self):
        r = requests.patch("{}/{}".format(urls.POSTS_URL, '1'))
        assert r.headers['Server'] == 'cloudflare'


class TestUserPostsDELETEMethod(object):
    def setup(self):
        # Checking site availability
        try:
            requests.get(urls.BASE_URL)
        except requests.ConnectionError:
            raise AssertionError("Connection Error Ocurred")

    def teardown(self):
        pass

    def test_posts_delete_by_user(self):
        for user in USERS:
            r = requests.delete("{}/{}".format(urls.POSTS_URL, user['id']))
            assert r.content == b'{}'
            assert r.status_code == 200

    def test_delete_wrong_user(self):
        r = requests.patch("{}/{}".format(urls.POSTS_URL, '1000'))
        assert r.content == b'{}'
        assert r.status_code == 404
