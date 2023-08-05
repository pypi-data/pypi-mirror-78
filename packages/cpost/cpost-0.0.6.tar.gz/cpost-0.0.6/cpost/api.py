# global
import warnings
import pkg_resources
import requests
# local
from . import _b2c as b2c

def regions():
    x = b2c.json('/services/Address/getRegionListAsJson')
    return {d['id']: d['name'] for d in x}
def districts(region_id = None):
    def _districts(region_id):
        params = {"id": int(region_id)}
        return b2c.json('/services/Address/getDistrictListAsJson', params=params)
    # a certain region
    if region_id is not None: x = _districts(region_id)
    # all regions
    else: x = [_districts(r) for r in regions()]
    return {d['id']: d['name'] for d in x}

def cities(district_id = None):
    def _cities(district_id):
        params = {"id": int(district_id)}
        return b2c.json('/services/Address/getCityListAsJson', params=params)
    # a certain district
    if district_id is not None: x = _cities(district_id)
    # all districts
    else: x = [_cities(d) for d in districts()]
    return [c for c in x]
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
