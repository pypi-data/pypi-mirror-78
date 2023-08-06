from typing import Any

from arpoc.plugins import _lib

import arpoc.utils

class EnvAttrTime(_lib.EnvironmentAttribute):
    """ 
    Returns the current time (UTC) in HH:MM:SS format

    Attribute key: time
    """

    target = "time"

    @staticmethod
    def run() -> Any:
        now = arpoc.utils.now_object()
        return "{:02d}:{:02d}:{:02d}".format(now.hour, now.minute, now.second)


class EnvAttrDateTime(_lib.EnvironmentAttribute):
    """
    Returns the current time (UTC) in YYYY-MM-DD HH:MM:SS format

    Attribute key: datetime
    """

    target = "datetime"

    @staticmethod
    def run() -> Any:
        now = arpoc.utils.now_object()
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(now.year,
                                                                  now.month,
                                                                  now.day,
                                                                  now.hour,
                                                                  now.minute,
                                                                  now.second)


class EnvAttrTimeHour(_lib.EnvironmentAttribute):
    """
    Returns the current hours of the clock (UTC)

    Attribute key: time_hour
    """

    target = "time_hour"

    @staticmethod
    def run() -> Any:
        now = arpoc.utils.now_object()
        return now.hour


class EnvAttrTimeMinute(_lib.EnvironmentAttribute):
    """
    Returns the current minute of the clock (UTC)

    Attribute key: time_minute
    """

    target = "time_minute"

    @staticmethod
    def run() -> Any:
        now = arpoc.utils.now_object()
        return now.minute


class EnvAttrTimeSecond(_lib.EnvironmentAttribute):
    """
    Returns the current second of the clock (UTC) 

    Attribute key: time_second
    """

    target = "time_second"

    @staticmethod
    def run() -> Any:
        now = arpoc.utils.now_object()
        return now.second
