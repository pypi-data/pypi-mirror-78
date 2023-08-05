
import functools
import pkg_resources
import sqlite3

def dbaccess(dbname):
    def dbaccess_wrapper(fn):
        @functools.wraps(fn)
        def fn_replace(*args, **kw):
            # connect
            fname = pkg_resources.resource_filename(__name__, dbname)
            conn = sqlite3.connect(fname)
            
            x = fn(conn.cursor(), *args, **kw) # run command
            
            conn.commit() # commit
            conn.close()
            return x
        return fn_replace
    return dbaccess_wrapper

bypass = lambda x: x
def tryInt(i):
    try: return int(i)
    except: i
city_cols = ['city_id','city_name','district_id','region_id']
city_f = [int, bypass, int, bypass, int, bypass]
address_cols = ['house_id','house_name','street_id','street_name','city_part_id','city_part_name','city_id']
address_f = [int, bypass, tryInt, bypass, int, bypass, int]


@dbaccess("data/data.db")
def _read_regions(c):
    c.execute('SELECT * FROM regions')
    x = c.fetchall()
    return {r[0]: r[1] for r in x}
@dbaccess("data/data.db")
def _read_districts(c):
    c.execute('SELECT * FROM districts')
    x = c.fetchall()
    return {d[0]: d[1] for d in x}
@dbaccess("data/data.db")
def read_cities(c):
    c.execute('SELECT * FROM cities')
    x = c.fetchall()
    regions,districts = _read_regions(),_read_districts()
    x = [{col: xij for col,xij in zip(city_cols,xi)} for xi in x]
    return [{**city,
             'region_name': regions[city['region_id']],
             'district_name': districts[city['district_id']]} for city in x]
#@dbaccess("data/data.db")
#def read_addresses(c):
#    c.execute('SELECT * FROM addresses')
#    x = c.fetchall()
#    return [{col: xij for col,xij in zip(address_cols,xi)} for xi in x]

# logger
import logging
_log = logging.getLogger(__name__)

__all__ = ["initialize",
           "insert_city","insert_address",
           "read_cities","read_addresses",
           "_read_regions","_read_districts"]