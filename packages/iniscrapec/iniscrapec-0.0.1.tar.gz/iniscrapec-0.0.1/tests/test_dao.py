from unittest import TestCase

from modules import Dao


class TestDao(TestCase):
    def test_functions(self):
        database = Dao()
        key = 123123
        value = 321321
        database.add(key, value)
        assert database.contains(key)
        assert database.get(key) == value
