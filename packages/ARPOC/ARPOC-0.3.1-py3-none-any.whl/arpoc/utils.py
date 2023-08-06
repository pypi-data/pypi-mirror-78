"""
ARPOC utils

Time functions that are used in ARPOC.
Can be swapped for unittests
"""
import datetime

def now_object():
    """ Return a datetime object with current timestamp"""
    return datetime.datetime.now()

def now():
    """ Return the seconds since begin of the EPOCH """
    return int(datetime.datetime.now().timestamp())
