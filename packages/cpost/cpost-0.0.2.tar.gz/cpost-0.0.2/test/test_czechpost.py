
from datetime import datetime
import unittest

import cpost


class TestCzechPost(unittest.TestCase):
    def test_regions(self):
        x = cpost._api.regions()
    def test_districts(self):
        x = cpost._api.districts(11)
    def test_cities(self):
        x = cpost._api.cities(55)
    def test_city_parts(self):
        x = cpost._api.city_parts(5185)
    def test_streets(self):
        x = cpost._api.streets(12501)
    def test_addresses(self):
        x = cpost._api.addresses(28783)
        print(x)

__all__ = ["TestCzechPost"]
        