
import requests
import urllib3

def get(path, *args, **kw):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    url = f'https://b2c.cpost.cz{path}'
    return requests.get(url, *args, **kw, verify=False)

def json(*args, **kw):
    return get(*args, **kw).json()

all = ["get","json"]
