from unittest import TestCase
import responses

from faker import Faker
from togglee.togglee import Togglee
import time

fake = Faker()


class ToggleTest(TestCase):
    def test_use_default_toggles(self):
        url = fake.url()
        prop_True = fake.pystr()
        prop_False = fake.pystr()
        fakeDict = {
            prop_True: True,
            prop_False: False
        }
        subject = Togglee(url, 100, fakeDict)
        assert subject.is_enabled(prop_True)
        assert not subject.is_enabled(prop_False)


    def test_return_false_as_default(self):
        prop = fake.pystr()
        subject = Togglee(fake.url(), fake.pyint(), {})
        assert not subject.is_enabled(prop)


    def test_return_false_if_no_defaults(self):
        prop = fake.pystr()
        subject = Togglee(fake.url(), fake.pyint(), None)
        assert not subject.is_enabled(prop)


    @responses.activate
    def test_refresh_cache_in_rate(self):
        url = fake.url()
        print(url)
        responses.add(responses.GET, url,
                      json={'prop': True}, status=200)
        subject = Togglee(url, 1, {})
        time.sleep(5)
        assert subject.is_enabled("prop")
