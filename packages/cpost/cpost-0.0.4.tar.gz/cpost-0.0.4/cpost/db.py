# global

# local
from . import _b2c as b2c
from . import _db

def regions():
    data = _db._read_regions()
    return data
def districts(region_id):
    data = _db._read_districts()
    data = filter(lambda i: i['region_id'] == region_id, data)
    return data
def cities(district_id):
    data = _db.read_cities()
    data = filter(lambda i: i['district_id'] == district_id, data)
    return sorted(data, key=lambda i: int(i['city_id']))

def city_parts(city_id):
    raise NotImplementedError
def streets(city_part_id):
    raise NotImplementedError
def addresses(street_id=None, city_part_id=None):
    raise NotImplementedError

__all__ = ["regions","districts","cities","city_parts","streets","addresses"]
