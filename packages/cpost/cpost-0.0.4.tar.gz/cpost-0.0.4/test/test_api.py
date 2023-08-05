
from datetime import datetime
import unittest

import cpost

class TestCzechPost(unittest.TestCase):
    def test_regions(self):
        x = cpost.api.regions()
    def test_districts(self):
        x = cpost.api.districts(11)
    def test_cities(self):
        x = cpost.api.cities(55)
    def test_city_parts(self):
        x = cpost.api.city_parts(5185)
    def test_streets(self):
        x = cpost.api.streets(12501)
    def test_addresses(self):
        x = cpost.api.addresses(28783)

__all__ = ["TestCzechPost"]
        