from unittest import TestCase

from iniscrapec import memoize
from modules import find_pec


class Test(TestCase):
    def test_memoize(self):
        memoized_func = memoize(find_pec)
        # Insert a valid tax code to see if the result is the same
        # assert memoized_func(12312312311) == find_pec(12312312311)
