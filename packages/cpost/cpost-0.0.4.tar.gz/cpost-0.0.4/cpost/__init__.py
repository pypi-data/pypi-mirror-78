# -*- coding: utf-8 -*-
"""API/Python lib for Czech addresses
 
Sources:
    * https://b2c.cpost.cz
Todo:
    * More sources
    * Caching
"""

import pkg_resources

from . import api
from . import db

try:
    __version__ = pkg_resources.get_distribution("cpost").version
except:
    __version__ = None
