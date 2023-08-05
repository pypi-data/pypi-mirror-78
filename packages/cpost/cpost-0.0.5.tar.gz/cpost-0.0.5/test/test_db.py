
import sys
import unittest

sys.path.append("..")

import cpost

class TestCzechPost(unittest.TestCase):
    def test_regions(self):
        x = cpost.db.regions()
    def test_districts(self):
        x = cpost.db.districts(11)
    def test_cities(self):
        x = cpost.db.cities(55)
    def test_city_parts(self):
        try:
            x = cpost.db.city_parts(5185)
        except: pass
    def test_streets(self):
        try:
            x = cpost.db.streets(12501)
        except: pass
    def test_addresses(self):
        try:
            x = cpost.db.addresses(28783)
        except: pass

__all__ = ["TestCzechPost"]
        