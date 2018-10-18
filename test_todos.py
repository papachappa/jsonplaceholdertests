import requests
import pytest

from settings import urls
from test_data import todos


class TestTODOsGETMethod(object):
    @pytest.fixture()
    def setup(self):
        # Checking site availability
        try:
            requests.get(urls.BASE_URL)
        except requests.ConnectionError:
            raise AssertionError("Connection Error Ocurred")
        else:
            return requests.get(urls.TODOS_URL)

    def teardown(self):
        pass

    def test_todos_quantity(self, setup):
        assert len(setup.json()) == todos.TODOS_OVERALL_QUANTITY

    def test_todos_user1_quantity(self):
        r = requests.get(urls.TODOS_URL, params=todos.user1_qty_payload)
        assert len(r.json()) == todos.TODOS_USER1_QUANTITY

    def test_todos_user1_title(self):
        r = requests.get(urls.TODOS_URL, params=todos.user1_title_payload)
        assert r.json()[0]['title'] == todos.user1_title

    def test_todos_completed(self):
        r = requests.get(urls.TODOS_URL, params=todos.todos_completed_payload)
        assert len(r.json()) == todos.TODOS_COMPLETED
