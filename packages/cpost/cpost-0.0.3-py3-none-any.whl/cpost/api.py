# global
import warnings
import pkg_resources
import requests
# local
from . import _b2c as b2c

def regions():
    data = b2c.json('/services/Address/getRegionListAsJson')
    return sorted(data, key=lambda i: int(i['id']))
def districts(region_id):
    params = {"id": int(region_id)}
    data = b2c.json('/services/Address/getDistrictListAsJson', params=params)
    return data
def cities(district_id):
    params = {"id": int(district_id)}
    data = b2c.json('/services/Address/getCityListAsJson', params=params)
    return data
def city_parts(city_id):
    params = {"id": int(city_id)}
    data = b2c.json('/services/Address/getCityPartListAsJson', params=params)
    return data
def streets(city_part_id):
    params = {"id": int(city_part_id)}
    data = b2c.json('/services/Address/getStreetListAsJson',params=params)
    return data
def addresses(street_id=None, city_part_id=None):
    path = '/services/Address/getNumberListAsJson'
    by_street = b2c.json(path, params={"idStreet": street_id}) if street_id else []
    by_part = b2c.json(path, params={"idCityPart": city_part_id}) if city_part_id else []
    data = [*by_street, *by_part]
    return data

__all__ = ["regions","districts","cities","city_parts","streets","addresses"]
